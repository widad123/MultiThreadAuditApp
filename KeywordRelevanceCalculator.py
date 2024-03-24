import threading

class KeywordRelevanceCalculator(threading.Thread):
    def __init__(self, keyword_frequency):
        threading.Thread.__init__(self)
        self.keyword_frequency = keyword_frequency if keyword_frequency is not None else {}
        self.keyword_relevance = {}

    def run(self):
        if self.keyword_frequency:
            for keyword, frequency in self.keyword_frequency.items():
                self.keyword_relevance[keyword] = frequency
            
            total_frequency = sum(self.keyword_relevance.values())
            num_keywords = len(self.keyword_relevance)
            self.average_relevance = total_frequency / num_keywords if num_keywords > 0 else 0
        else:
            self.average_relevance = 0
