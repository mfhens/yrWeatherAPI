<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    
    <xsl:output method="html" doctype-public="XSLT-compat" omit-xml-declaration="yes" encoding="UTF-8" indent="yes" />

    <xsl:template match="/weatherdata">
        <html class="yr" lang="en-gb">
            <head>
                <xsl:value-of select="location/name/text()"/>, <xsl:value-of select="location/country/text()"/> 
            </head>
            <body>
                <xsl:copy-of select="credit/link"/>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>