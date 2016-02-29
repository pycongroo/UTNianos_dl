from bs4 import BeautifulSoup as Bs
import sys
sys.path.append("externals/pynet")
import pynet as net


URL_BASE = 'http://www.utnianos.com.ar/foro/'


def download_attachments(post_url):
    links = get_url_attachments(post_url)
    for link in links:
        net.download_file(link)


def get_url_attachments(post_url):
    utn_text = net.request_get(post_url).text
    utn_soup = Bs(utn_text)
    att_img = utn_soup.findAll('img', {'class': 'attachment'})
    img_links = map(lambda tag: URL_BASE + tag.get('src'), att_img)
    att_tag = utn_soup.findAll('a', {'name': 'download'})
    att_links = map(lambda tag: URL_BASE + tag.get('href'), att_tag)
    return img_links + att_links
