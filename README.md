DataSync web service connector
==============================

This is a simple base connector for Novell Data Synchronizer to connect applications like Novell GroupWise to a REST web service. Using this connector, you can integrate products like GroupWise with a variety of applications, like CRM systems, calendar applications, mail scanners, etc. You can use this connector as a base for custom integrations.

Prerequisites
-------------

To build a succesful connector you'll need at least:

* An installed and configured [Novell Data Synchronizer 1.2.x](http://download.novell.com/Download?buildid=AwGj_CBABEI~) (do **not install** Mobility Pack on it!)
* An editor to edit Python
* A webservice which you would like to connect
* SSH connection to the Data Synchronizer service to read logfiles and to restart Data Synchronizer

Applications
------------

The following applications are known to use this connector:

* This connector was the base connector for the [CalendarSync](http://www.interexperts.nl/english/solutions/data-synchronizer-connectors/calendarsync) application, which reads calendar events from a GroupWise installation and publishes these in a nice web interface.
* InterExperts has used this plug-in to integrate some internal systems with GroupWise.

Tips
----

* Use [multitail](http://www.vanheusden.com/multitail/) to watch the Data Synchronizer log files.
  Use the provided [multitailrc](contrib/multitailrc) to get fancy log files and use a command like:
  `multitail -cS dsconnector /var/log/datasync/connectors/default.pipeline1.yourconnector-AppInterface.log`
* Restart the Data Synchronizer engine using the following commands:  
  `/etc/init.d/datasync-connectors stop && /etc/init.d/datasync-syncengine stop`  
  `/etc/init.d/datasync-syncengine start && /etc/init.d/datasync-connectors start`

Resources
---------

See for more information about developing a Data Synchronizer connector also:

* [Novell Data Synchronizer Developer Kit](https://www.novell.com/developer/ndk/datasynchronizer.html) for general documentation about
  Data Synchronizer and developing connectors.
* [GroupWise Web Service (SOAP)](https://www.novell.com/developer/ndk/groupwise/groupwise_web_service_%28soap%29.html) which is useful
  when you are developing a connector which interacts with GroupWise.

License
-------

The connector provided on GitHub is developed by [InterExperts](http://www.interexperts.nl/) and provided as open source, licensed under the MIT license. Pull requests to enhance this connector are welcome!