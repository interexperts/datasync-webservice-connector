<!-- HTML template for connector settings. -->

<!-- httpHost -->
<tr>
        <td class="label">HTTP Host
                <span class="tooltip_container">
                        <img src="style/images/icons/help_tooltip.png" class="help_icon" title="Enter the hostname (FQDN) or IP address of the HTTP server running the webservice.">
                </span>
        </td>
        <td class="element">
                <input name="customsetting_httpServer" id="customsetting_httpServer" class="customsetting_text" type="text" size="50"/>
        </td>
</tr>

<!-- httpPort -->
<tr>
        <td class="label">HTTP(S) Port
                <span class="tooltip_container">
                        <img src="style/images/icons/help_tooltip.png" class="help_icon" title="Define which port to use (usually 80, or 443 for HTTPS).">
                </span>
        </td>
        <td class="element">
                <input name="customsetting_httpPort" id="customsetting_httpPort" class="customsetting_text" type="text" size="5"/>
        </td>
</tr>

<!-- httpUseSSL -->
<tr>
        <td class="label">
                Use secure SSL connection
                <span class="tooltip_container">
                        <img src="style/images/icons/help_tooltip.png" class="help_icon" title="Check this box to use a SSL connection.">
                </span>
        </td>
        <td class="element">
                <input name="customsetting_httpUseSSL" id="customsetting_httpUseSSL" class="customsetting_checkbox" type="checkbox" checked="false"/>
        </td>
</tr>

<!-- httpEndPoint -->
<tr>
        <td class="label">
                Webservice URL endpoint
        <span class="tooltip_container">
            <img src="style/images/icons/help_tooltip.png" class="help_icon" title="Enter the URL endpoint. Usually, the endpoint URL should end with a '/'.">
        </span>
        </td>
        <td class="element">
                <input name="customsetting_httpEndPoint" id="customsetting_httpEndPoint" class="customsetting_text" type="text" size="30"/>
        </td>
</tr>

<!-- httpAuthKey -->
<tr>
        <td class="label">
				Security key
        <span class="tooltip_container">
            <img src="style/images/icons/help_tooltip.png" class="help_icon" title="Enter the security key. This key has to match the security key of the webservice.">
        </span>
        </td>
        <td class="element">
                <input name="customsetting_httpAuthKey" id="customsetting_httpAuthKey" class="customsetting_text" type="text" size="30"/>
        </td>
</tr>

<!-- gwConnectorID -->
<tr>
        <td class="label">
                GroupWise Connector ID (e.g. default.pipeline1.groupwise)
        <span class="tooltip_container">
            <img src="style/images/icons/help_tooltip.png" class="help_icon" title="Enter the GroupWise Connector ID.">
        </span>
        </td>
        <td class="element">
            <input name="customsetting_gwConnectorID" id="customsetting_gwConnectorID" class="customsetting_text" type="text" size="30"/>
        </td>
</tr>