from bs4 import BeautifulSoup
import threading

class AltTagsChecker(threading.Thread):
    def __init__(self, html):
        threading.Thread.__init__(self)
        self.html = html
        self.missing_alt_count = 0 

    def run(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        img_tags = soup.find_all('img')
        self.missing_alt_count = sum(1 for img_tag in img_tags if not img_tag.get('alt'))
