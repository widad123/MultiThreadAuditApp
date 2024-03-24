from bs4 import BeautifulSoup
import threading

class H1TagsExtractor(threading.Thread):
    def __init__(self, html):
        threading.Thread.__init__(self)
        self.html = html
        self.h1_tags = None

    def run(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        self.h1_tags = [h1_tag.text.strip() for h1_tag in soup.find_all('h1')]