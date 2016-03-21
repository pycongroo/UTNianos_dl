from bs4 import BeautifulSoup as Bs
import sys
import os
sys.path.append("externals/pynet")
import pynet as net


URL_BASE = 'http://www.utnianos.com.ar/foro/'
DOWNLOAD_PATH = 'descargas'


def download_attachments(post_url):
    """Descarga todos los adjuntos del post."""
    try:
        os.mkdir(DOWNLOAD_PATH)
    except:
        print "%s/ OK" % DOWNLOAD_PATH
    path_post = post_url.rsplit('/')[-1]
    try:
        print "Creando directorio %s" % path_post
        os.mkdir("%s/%s" % (DOWNLOAD_PATH, path_post))
    except:
        print "ya existe directorio"
    attachments = get_attachments(post_url)
    for i in range(len(attachments)):
        print "Descargando adjunto %s de %s" % (
            str(i + 1),
            str(len(attachments)))
        net.download_file(
            attachments[i]['url'],
            "%s/%s/%s" % (
                DOWNLOAD_PATH,
                path_post, attachments[i]['name']))


def corregir_adjuntos(post_url):
    """Otorga los nombres reales a los adjuntos
    (Problema de la primera version)."""
    path_post = post_url.rsplit('/')[-1]
    attachments = get_attachments(post_url)
    for i in range(len(attachments)):
        print "cambiando de %s a %s" % (str(i), attachments[i]['name'])
        old = '%s/%s/%s' % (DOWNLOAD_PATH, path_post, str(i))
        new = '%s/%s/%s' % (DOWNLOAD_PATH, path_post, attachments[i]['name'])
        print "Antiguo: %s" % old
        print "Nuevo: %s" % new
        os.rename(old, new)


def get_attachments(post_url):
    """Obtiene los links de los adjuntos en el post."""
    dict_list = []
    utn_text = net.request_get(post_url).text
    utn_soup = Bs(utn_text,'lxml')
    att_img = utn_soup.findAll('img', {'class': 'attachment'})
    img_links = map(lambda tag: URL_BASE + tag.get('src'), att_img)
    for i in range(len(img_links)):
        dict_list.append({
            'name': "%s.jpg" % str(i),
            'url': img_links[i]})
    att_tag = utn_soup.findAll('a', {'name': 'download'})
    for i in range(len(att_tag)):
        dict_list.append({
            'name': att_tag[i].getText(),
            'url': URL_BASE + att_tag[i].get('href')})
    print "Encontrados %s adjuntos!!!" % str(len(dict_list))
    return dict_list


if (len(sys.argv) > 1):
    posts = sys.argv[1:]
    for post in posts:
        download_attachments(post)
else:
    print("Debe ingresar las direcciones de los post separados por espacios!")
    print("python UTNianos_dl.py [URL_POST]...")
