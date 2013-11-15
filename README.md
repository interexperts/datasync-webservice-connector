Webservice connector for Novell Data Synchronizer
=================================================

This is a simple connector for Novell Data Synchronizer, to connect applications like Novell GroupWise to a REST web service. Using this connector, you can integrate products like GroupWise with a variety of applications, like CRM systems, calendar applications, mail scanners, etc. You can use this connector as a base for custom integrations.

Prerequisites
-------------

To build a succesful connector you'll need at least:

* An installed and configured [Novell Data Synchronizer 1.2.x](http://download.novell.com/Download?buildid=AwGj_CBABEI~) (**not** Mobility Pack)
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
* Restart the Data Synchronizer engine using the following commands:
  ```
  /etc/init.d/datasync-connectors stop && /etc/init.d/datasync-syncengine stop
  /etc/init.d/datasync-syncengine start && /etc/init.d/datasync-connectors start
  ```

License
-------

The connector provided on GitHub is developed by [InterExperts](http://www.interexperts.nl/) and provided as open source, licensed under the MIT license. Pull requests to enhance this base connector are welcome!