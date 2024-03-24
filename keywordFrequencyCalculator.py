import threading
from bs4 import BeautifulSoup

class KeywordFrequencyCalculator(threading.Thread):
    def __init__(self, html, keywords):
        threading.Thread.__init__(self)
        self.html = html
        self.keywords = keywords
        self.keyword_frequency = {}

    def run(self):
        # Utiliser BeautifulSoup pour extraire le texte à partir du HTML
        soup = BeautifulSoup(self.html, 'html.parser')
        text = soup.get_text().lower()
        words = text.split()
        
        # Calculer le nombre total de mots
        total_words = len(words)

        # Calculer la fréquence de chaque mot-clé
        for keyword in self.keywords:
            # Compter le nombre d'occurrences du mot-clé dans le texte
            count = text.count(keyword.lower())
            # Calculer la fréquence du mot-clé
            frequency = count / total_words if total_words > 0 else 0
            self.keyword_frequency[keyword] = frequency
