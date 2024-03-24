import time
import requests
import threading

class PageLoadTimeCalculator(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url
        self.load_time = None

    def run(self):
        try:
            start_time = time.time()
            requests.get(self.url)
            end_time = time.time()
            self.load_time = end_time - start_time
        except Exception as e:
            print(f"Error occurred while calculating page load time for {self.url}: {str(e)}")