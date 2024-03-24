from bs4 import BeautifulSoup
import threading

class VideoInfoExtractor(threading.Thread):
    def __init__(self, html):
        threading.Thread.__init__(self)
        self.html = html
        self.videos_info = None

    def run(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        video_tags = soup.find_all('video')
        self.videos_info = [{'src': video_tag.get('src')} for video_tag in video_tags]