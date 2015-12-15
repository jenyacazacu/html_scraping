import sys

# requires a separate installation of the below libraries
# pip install lxml, pip install requests
from lxml import html
import requests

def parse_html(url):
	
	try:
		# get the html page
		html_page = requests.get(url)
	except Exception as e:
		print 'Error while trying to get the web page: {0}'.format(e)
	
	try:
 		#parse the data into a tree
		tree = html.fromstring(html_page.content)
	except Exception as e:
		print 'Error while trying to parse the html page to a tree: {0}'.format(e)
	
	images = tree.xpath("//img")
	javascript = tree.xpath("//script[starts-with(@src, 'http') or starts-with(@src, '//')]")
	css_files = tree.xpath("//link[starts-with(@href, 'http') or starts-with(@href, '//') and  @rel='stylesheet']")
	external_urls = tree.xpath("//a[starts-with(@href,'http') or starts-with(@href, '//')]")
	
	image_list = get_images(images)
	javascript_list = get_external_javascript(javascript)
	css_list = get_css(css_files)
	urls_list = get_external_urls(external_urls)
	
	print_args = (image_list, javascript_list, css_list, urls_list)

	print '\nImages: {0} \n\nExternal JavaScript: {1} \n\nExternal CSS: {2} \n\nExternal Links: {3}'.format(*print_args)


def get_images(img_elements):
	img_list = [img.attrib['src'] for img in img_elements]
	return img_list
	

def get_external_javascript(js_elements):
	js_list = [js.attrib['src'] for js in js_elements]
	return js_list

def get_css(css_elements):
	css_list = [css.attrib['href'] for css in css_elements]
	return css_list

def get_external_urls(url_elements):
	url_list = [url.attrib['href'] for url in url_elements] 
	return url_list
	

if __name__=="__main__":
	if len(sys.argv) <= 1:
		print("You must include a url, ex 'python html_parser.py https://wwww.google.com'")
	else:
		parse_html(sys.argv[1])

