#!/usr/bin/python

import os
import sys
import superxml
import datasync
import syncengine
import syncengine.GenericApplicationInterface as GenericAI

import urllib
import urllib2
import lxml
import lxml.etree
import string

import datetime

from time import gmtime, strftime

class ApplicationInterface(GenericAI.GenericApplicationInterface):
	# Connector version
	connectorVersion = '1.0.0'

	# Connection details:
	httpHost = '127.0.0.1'
	httpPort = 80
	httpEndPoint = '/'
	httpUseSSL = False
	httpAuthKey = 'changeme'

	# Connector ID:
	connectorID = None
	
	# Be verbose in logging messages?
	verboseLogging = False

	def __init__(self):
		"""
		Initialization of the ApplicationInterface.
		"""
		GenericAI.GenericApplicationInterface.__init__(self)


	def startup(self, config):
		"""
		Called when the connector starts up.
		"""
		# Store configuration in our own object
		self.connectorConfig = config.getDict()

		# Log some information about the connector.
		self.logger.info('DataSync web service connector version %s'  % self.connectorVersion)
		self.logger.info('Copyright (c) 2013 InterExperts BV and provided under MIT license')
		self.logger.info('Connector starting up...')

		# Parse connector configuration:
		try:
			self.parseConnectorConfig(config)
		except ConnectorConfigurationError as configError:
			# Uncatched exception thrown while loading configuration: configuration error. Prevent connector startup.
			self.logger.info('Loading configuration failed.')
			self.logException()
			self.logger.info('Connector not starting up due to config error.')
			return 'Loading configuration failed, configuration error in %s: %s' % (configError.var, configError.msg)
		except:
			# Uncatched exception thrown while loading configuration: probably an configuration error. Prevent connector startup.
			self.logger.info('Loading configuration failed.')
			self.logException()
			self.logger.info('Connector not starting up.')
			return 'Loading configuration failed.'

		# Configuration successfully loaded, continue starting connector.
		self.logger.info('Configuration loaded.')
		
		self.status = 'Started'
		
		# All went OK, return Success:
		return 'Success'


	def shutdown(self):
		"""
		Shut down the connector.
		Returns 'Success' if connector is started successfully, otherwise a string with an error message.
		"""
		self.logger.info('Shut down...')
		self.status = 'Stopped'

		return 'Success'


	def parseConnectorConfig(self, config):
		"""
		Parse the configuration supplied in config.
		An ConnectorConfigurationError exception is raised when there is an error in the connector config.
		"""
		self.logger.debug('Parsing configuration. XML config: %s' % config)
		
		self.httpHost = config.root.settings.custom.httpServer.text
		self.httpPort = config.root.settings.custom.httpPort.text
		self.httpEndPoint = config.root.settings.custom.httpEndPoint.text
		self.httpAuthKey = config.root.settings.custom.httpAuthKey.text

		self.httpPort = int(self.httpPort)
		if (self.httpPort <= 0):
			raise ConnectorConfigurationError('httpPort', 'Server port number must be a non-negative integer.')

		if (config.root.settings.custom.httpUseSSL.text == '1' or config.root.settings.custom.httpUseSSL.text == 'true'):
			self.httpUseSSL = True
			self.logger.debug('Using a secure SSL connection.')
		else:
			self.httpUseSSL = False
			self.logger.debug('Not using a secure SSL connection.')

		# Set verbose logging on or off:
		if (config.root.settings.common.log.verbose.text == '1' or config.root.settings.common.log.verbose.text == 'true'):
			self.verboseLogging = True
		else:
			self.verboseLogging = False

		try:
			self.connectorID = config.root.id.text
		except:
			# Connector ID is not provided when configuration is changed, it's only passed during connector startup.
			pass

		# Configuration loaded without errors:
		return


	def startAppConnection(self):
		"""
		Starts the application connection.
		"""
		return 'Success'

	def startAppListener(self):
		"""
		Starts the application listener.
		"""
		return 'Success'
	
	def engineEventReceived(self, event, processDepth):
		"""
		Process newly received events (originating from the datasync engine).
		@param event The SuperXML object of the event to be processed.
		@return 'Success' if the event is processed successfully, 'Error' when the item type or event type is not supported or when an error occurred during event processing.
		"""
		if self.status == 'Stopped':
			self.logger.debug('Connector stopped, ignoring event')
			return 'Connector stopped'

		self.logger.debug("Event received from the engine.")
		
		# Parse the event and dispatch to the proper method
		eventType = event.root.metadata.type.text.capitalize()
		itemType = event.root.item.get('type').capitalize()

		# Log full event for debugging purposes:
		self.logger.debug("itemType = %s, eventType = %s" % (itemType, eventType))

		# Event is added:
		if eventType == 'Add':
			objectID = 'datasync-%s' % event.root.metadata.id.text
			result = self.eventAdded(event, objectID)

			# Send feedback to engine.
			if result == 'Success':
				# Subscribe to this event with the above ojectID:
				self.sendStatus(event, objectID, 'Success')
			else:
				# Inform engine that sync event failed. Engine will send event again later
				self.sendStatus(event, objectID, 'Failed')

			return

		elif eventType == 'Modify':
			objectID = 'datasync-%s' % event.root.metadata.id.text
			result = self.eventModified(event)
			
			# Send feedback to engine.
			if result == 'Success':
				# Inform sync engine that this event was processed successfully.
				self.sendStatus(event, objectID, 'Success')
			else:
				# Inform engine that sync event failed. Engine will send event again later
				self.sendStatus(event, objectID, 'Failed')

			return

		elif eventType == 'Delete':
			objectID = 'datasync-%s' % event.root.metadata.id.text
			result = self.eventDeleted(event)

			# Send feedback to engine.
			if result == 'Success':
				# Inform sync engine that this event was processed successfully.
				self.sendStatus(event, objectID, 'Success')
			else:
				# Inform engine that sync event failed. Engine will send event again later
				self.sendStatus(event, objectID, 'Failed')

			return
		else:
			self.logger.debug("Item with type = %s, eventType = %s not supported by this connector." % (itemType, eventType))

		return 'Error: Event not supported by this connector'


	def getInfo(self):
		"""
		Returns information about the connector
		@return A dictionary containing the connector version (key: 'version) and the connector
		status (key: 'status', possible values: 'Started' or 'Stopped')
		"""
		return {'version' : self.connectorVersion, 'status': self.status}


	def sendDataToWebService(self, data):
		"""
		Send data to webservice.
		"""
		# Define protocol (http/https):
		if (self.httpUseSSL == True):
			protocol = 'https'
		else:
			protocol = 'http'

		# Build base URL by using protocol, host, port and API endpoint: 
		baseURL = '%s://%s:%s%s' % (protocol, self.httpHost, self.httpPort, self.httpEndPoint)

		# Add HTTP auth key to data dictionary:
		data['auth_key'] = self.httpAuthKey

		# Encode data parameters:
		for key in data:
			if data[key] != None:
				data[key] = data[key].encode('utf-8')
			else:
				data[key] = ''

		data = urllib.urlencode(data)

		# Define headers:
		headers = {
			'User-Agent': 'DataSync Webservice connector (Unix; U; rv:%s)' % self.connectorVersion,
			'Accept-Charset': 'utf-8',
			'Connection': 'keep-alive'
		}

		self.logger.debug("Sending data using the following URL: %s" % baseURL)
		
		req = urllib2.Request(baseURL, data, headers)
		response = urllib2.urlopen(req)

		return response.read()


	def eventAdded(self, event, objectID):
		"""
		This method is called whenever an event is added.
		event is the event (SuperXML) object supplied by the sync engine.
		The event is sent to the webservice.
		"""
		self.logger.debug("Received the following add event: %s" % event.getString())

		data = {}

		data['type'] = 'add'
		data['sourceDN'] = event.root.metadata.sourceName.text
		data['timestamp'] = event.root.metadata.timestamp.text
		data['itemID'] = objectID
		data['event'] = event.getString()

		# Send to webservice
		result = self.sendDataToWebService(data)

		try:
			resultXml = superxml.fromString(result)
		except:
			self.logger.error("Received invalid response from webservice. Event not synced correctly.")
			return "Error"

		if (resultXml.root.status.text == 'OK'):
			self.logger.debug("Item synced succesfully.")
			return "Success"
		else:
			self.logger.error("Remote webservice returned the following error: %s" % resultXml.root.message.text)
			return "Error"

		return "Success"


	def eventModified(self, event):
		"""
		Called when an modify event is received.
		This method sends all relevant properties to the webserivce.
		An event is identified by the objectID to which it is subscribed.
		"""
		self.logger.debug("Received the following modify event: %s" % event.getString())

		data = {}
		data['type'] = 'modify'
		data['itemID'] = event.root.metadata.objectID.text
		data['timestamp'] = event.root.metadata.timestamp.text
		data['event'] = event.getString()

		# Send to webservice
		result = self.sendDataToWebService(data)
		
		try:
			resultXml = superxml.fromString(result)
		except:
			self.logger.error("Received invalid response from webservice. Event not synced correctly.")
			return "Error"
		
		if (resultXml.root.status.text == 'OK'):
			self.logger.debug("Item synced succesfully.")
			return "Success"
		else:
			self.logger.error("Remote webservice returned the following error: %s" % resultXml.root.message.text)
			return "Error"
	
	
	def eventDeleted(self, event):
		"""
		Called when an event is deleted.
		The webservice is informed that an event with the given itemID is deleted.
		"""
		self.logger.debug("Received the following delete event: %s" % event.getString())
		
		data = {
				'itemID':       event.root.metadata.objectID.text,
				'type':         'delete'
			}
		
		result = self.sendDataToWebService(data)
		
		try:
			resultXml = superxml.fromString(result)
		except:
			self.logger.error("Received invalid response from webservice. Event not synced correctly.")
			return "Error"
		
		if (resultXml.root.status.text == 'OK'):
			self.logger.debug("Item synced succesfully.")
			return "Success"
		else:
			self.logger.error("Remote webservice returned the following error: %s" % resultXml.root.message.text)
			return "Error"
	
	
	def targetSettingsChanged(self, targetDN, targetType, settingsXML):
		self.logger.debug('Got a targetSettingsChanged event for %s.' % targetDN)


	def targetAdded(self, targetDN, targetType, targetApplicationName):
		"""
		This method is called when a new target (=user) is added to the connector.
		This event is ignored when another targetType is added (i.e. a group).
		When a group is added, targetAdded() will be called for all group members, so usually we can ignore the group.
		"""
		if (targetType != 'user'):
			return
		else:
			self.logger.debug('New user added to the connector! Application name = %s' % targetApplicationName)


	def targetRemoved(self, targetDN, targetType, targetApplicationName):
		"""
		Called when a target (user) is removed.
		"""
		self.logger.debug('Target removed: %s (type=%s, applicationName=%s).' % (targetDN, targetType, targetApplicationName))


	def targetNameChanged(self, targetDN, targetType, targetApplicationNameOld, targetApplicationNameNew):
		self.logger.debug('Got a targetNameChanged event for %s: old %s, new %s.' % (targetDN, targetApplicationNameOld, targetApplicationNameNew))

   
	def connectorConfigChanged(self, settingsXML):
		"""
		Process changed configuration
		This method is called by the ApplicationInterface when the configuration is changed.
		This method calls parseConnectorConfig() to process the new configration.
		"""
		self.logger.debug('connectorConfigChanged invoked; parsing new configuration.')

		# Parse new configuration:
		self.parseConnectorConfig(settingsXML)


## Exception object raised for configuration errors.
class ConnectorConfigurationError(Exception):
	## Configuration variable in which the error occurred.
	var = None
	## Explanation of the error.
	msg = None

	## Constructor for ConnectorConfigurationError.
	# @param var Configuration variable in which the error occurred.
	# @param msg Explanation of the error.
	def __init__(self, var, msg):
		self.var = var
		self.msg = msg


if __name__ == '__main__':
	g = ApplicationInterface()
