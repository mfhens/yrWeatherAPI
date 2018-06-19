import urllib.request
import configparser
import yrconfig
from lxml import etree

url_prefix = yrconfig.url_prefix
url_pattern = yrconfig.url_pattern
yr_xml = yrconfig.xml
location = yrconfig.location

def generateUrl(urlPattern, fullLocation):
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

def retrieveForecastXml(fullLocation):
    url = generateUrl(url_pattern, fullLocation) + yr_xml
    response = urllib.request.urlopen(url)
    forecast = response.read()
    return forecast

def retrieveForecastHtml(fullLocation):
    url = generateUrl(url_pattern, fullLocation)
    response = urllib.request.urlopen(url)
    forecast = response.read()
    return forecast

def remove_unnecessary(htmltree):
    for node in htmltree.xpath("//div[starts-with(@class, 'yr-webcams')]"):
        node.getparent().remove(node)
    for node in htmltree.xpath("//header"):
        node.getparent().remove(node)
    for node in htmltree.xpath("//div[starts-with(@class, 'yr-footer')]"):
        node.getparent().remove(node)
    for node in htmltree.xpath("//div[starts-with(@class, 'yr-breadcrumbs')]"):
        node.getparent().remove(node)
    for node in htmltree.xpath("//li[@class='related']"):
        node.getparent().remove(node)
    for node in htmltree.xpath("//div[@id='yr-timestamp-tools']"):
        node.getparent().remove(node)
    for node in htmltree.xpath("//div[starts-with(@class, 'yr-pointinfo')]"):
        node.getparent().remove(node)
    for node in htmltree.xpath("//div[starts-with(@class, 'yr-map')]"):
        node.getparent().remove(node)
    return htmltree

def prefix_links(htmltree):
    for node in htmltree.xpath("//link[@rel='stylesheet']"):
        node.attrib['href'] = url_prefix + node.attrib['href']
    for node in htmltree.xpath("//img"):
        node.attrib['src'] = url_prefix + node.attrib['src']
    return htmltree

try:
    forecast = retrieveForecastHtml(location)
    parser = etree.HTMLParser()
    htmltree = etree.fromstring(forecast, parser)
    htmltree = remove_unnecessary(htmltree)
    htmltree = prefix_links(htmltree)
    htmlPage = open("test.html", "wb")
    htmlPage.write(etree.tostring(htmltree, pretty_print=True, method="HTML"))
except RuntimeError as error:
    print("Can't read forecast: {0}".format(error))
