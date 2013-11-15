<?xml version='1.0' encoding='utf-8'?>
<xsl:stylesheet version='1.0' 
	xmlns:xsl='http://www.w3.org/1999/XSL/Transform'
	xmlns:datasync='http://www.novell.com/nsxml/datasync/com.novell.datasync.syncengine.xslt.api'>
	<xsl:variable name="sourceDN" select="string(/event/metadata/sourceDN)"/>
	<xsl:variable name="isEnabled" select="datasync:isTargetEnabled($sourceDN)"/>
	<xsl:variable name="isTargetAdd" select="/event/metadata/type = 'addTargetToConnector'"/>
	<xsl:template match="event/metadata">
		<xsl:variable name="sourceName" select="substring-before(substring-after(./sourceDN,'cn='),',')"/>
		<xsl:copy>
			<xsl:apply-templates select="node()|@*"/>
			<sourceName><xsl:value-of select="$sourceName"/></sourceName>
		</xsl:copy>
	</xsl:template>

	<xsl:template match="node()|@*">
		<xsl:choose>
			<xsl:when test="$isTargetAdd or $isEnabled">
				<!-- copy event -->
				<xsl:copy>
					<xsl:apply-templates select="node()|@*"/>
				</xsl:copy>
			</xsl:when>
			<xsl:otherwise>
				<!-- drop event -->
				<xsl:value-of select="datasync:logMessage(concat('DN ', $sourceDN ,' is not enabled, dropping event'), 'debug')" />
			</xsl:otherwise>
		</xsl:choose>	
	</xsl:template>
</xsl:stylesheet>