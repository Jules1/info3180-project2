import requests
from bs4 import BeautifulSoup
import urlparse

url = "http://www.istockphoto.com/stock-photos"
result = requests.get(url)
soup = BeautifulSoup(result.text, "html.parser")
imgList = []

# This will look for a meta tag with the og:image property
og_image = (soup.find('meta', property='og:image') or
                    soup.find('meta', attrs={'name': 'og:image'}))
if og_image and og_image['content']:
    imgList.append(og_image['content'])

# This will look for a link tag with a rel attribute set to 'image_src'
thumbnail_spec = soup.find('link', rel='image_src')
if thumbnail_spec and thumbnail_spec['href']:
    imgList.append(thumbnail_spec['href'])


image = "%s"
for img in soup.findAll("img", src=True):
   imgList.append(image % urlparse.urljoin(url, img["src"]))
#print imgList

def listing():
	return imgList