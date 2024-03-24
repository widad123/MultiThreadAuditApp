from bs4 import BeautifulSoup
import requests
import threading


class SubPageAuditor(threading.Thread):
    def __init__(self, main_url):
        threading.Thread.__init__(self)
        self.main_url = main_url
        self.sub_pages = None

    def run(self):
        try:
            response = requests.get(self.main_url)
            if response.status_code == 200:
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                links = soup.find_all('a', href=True)
                self.sub_pages = [link.get('href') for link in links if link.get('href').startswith('http')]
            else:
                print(f"Failed to fetch HTML for {self.main_url}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Exception occurred while fetching HTML for {self.main_url}: {str(e)}")