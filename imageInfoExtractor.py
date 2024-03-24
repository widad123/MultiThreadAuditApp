from bs4 import BeautifulSoup
import threading

class ImageInfoExtractor(threading.Thread):
    def __init__(self, html):
        threading.Thread.__init__(self)
        self.html = html
        self.images_info = None

    def run(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        img_tags = soup.find_all('img')
        self.images_info = [{'src': img_tag.get('src'), 'alt': img_tag.get('alt', '')} for img_tag in img_tags]