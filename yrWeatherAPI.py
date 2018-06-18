import urllib.request
from lxml import etree

urlPattern = "http://www.yr.no/place/{}/forecast.xml"
location = "Denmark/Zealand/Asnæs"
xsltFilePath = "transformToHTML.xslt"

def generateUrl(fullLocation):
    fullLocation = properEncode(fullLocation)
    return urlPattern.format(fullLocation)

def properEncode(url):
  url = url.replace("ø", "%C3%B8")
  url = url.replace("å", "%C3%A5")
  url = url.replace("æ", "%C3%A6")
  url = url.replace("Ø", "%C3%98")
  url = url.replace("Å", "%C3%A5")
  url = url.replace("Æ", "%C3%85")
  return url

def retrieveForecast(fullLocation):
    url = generateUrl(fullLocation)
    response = urllib.request.urlopen(url)
    forecast = response.read()
    return forecast

try:
    forecast = retrieveForecast(location)
    root = etree.fromstring(forecast)
    xslt_doc = etree.parse(xsltFilePath)
    transform = etree.XSLT(xslt_doc)
    result = transform(root)
    print(result)
except RuntimeError as error:
    print("Can't read forecast: {0}".format(error))
