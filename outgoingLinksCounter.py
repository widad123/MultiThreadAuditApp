from bs4 import BeautifulSoup
import threading

class OutgoingLinksCounter(threading.Thread):
    def __init__(self, html):
        threading.Thread.__init__(self)
        self.html = html
        self.outgoing_links = None

    def run(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        links = soup.find_all('a', href=True)
        self.outgoing_links = len(links)