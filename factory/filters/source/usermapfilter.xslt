<?xml version='1.0' encoding='utf-8'?>
<xsl:stylesheet version='1.0' 
	xmlns:xsl='http://www.w3.org/1999/XSL/Transform'
	xmlns:datasync='http://www.novell.com/nsxml/datasync/com.novell.datasync.syncengine.xslt.api'>
    <xsl:variable name="sourceName" select="/event/metadata/sourceName"/>
	<xsl:variable name="sourceDN" select="datasync:getMatchingUserDN($sourceName)"/>
	
	<xsl:template match="event/metadata">
		<xsl:copy>
			<xsl:apply-templates select="node()|@*"/>
			<sourceDN><xsl:value-of select="$sourceDN"/></sourceDN>
		</xsl:copy>
	</xsl:template>
	<!-- veto event if the CN doesn't exist in the user containers on the directory -->
	<xsl:template match="node()|@*">
		<xsl:choose>
			<xsl:when test="string($sourceDN)">
				<!-- copy event -->
				<xsl:copy>
					<xsl:apply-templates select="node()|@*"/>
				</xsl:copy>
			</xsl:when>
			<xsl:otherwise>
				<!-- drop event -->
				<xsl:value-of select="datasync:logMessage(concat('User ', $sourceName, ' was not found or there are duplicate users in LDAP, dropping event'), 'warning')" />
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
</xsl:stylesheet>
