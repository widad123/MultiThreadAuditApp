import requests
import threading

class HTMLFetcher(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url
        self.html = None

    def run(self):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                self.html = response.text
            else:
                print(f"Failed to fetch HTML for {self.url}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Exception occurred while fetching HTML for {self.url}: {str(e)}")