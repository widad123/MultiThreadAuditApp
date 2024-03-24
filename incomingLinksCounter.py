from bs4 import BeautifulSoup
import threading

class IncomingLinksCounter(threading.Thread):
    def __init__(self, html, target_url):
        threading.Thread.__init__(self)
        self.html = html
        self.target_url = target_url
        self.incoming_links = None

    def run(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        links = soup.find_all('a', href=True)
        self.incoming_links = sum(1 for link in links if link.get('href').startswith(self.target_url))