from tkinter import ttk, messagebox
import tkinter as tk
from fpdf import FPDF
from pandastable import Table
import pandas as pd

# Import des autres modules nécessaires
from h1TagsExtractor import H1TagsExtractor
from altTagsChecker import AltTagsChecker
from htmlFetcher import HTMLFetcher
from imageInfoExtractor import ImageInfoExtractor
from incomingLinksCounter import IncomingLinksCounter
from keywordFrequencyCalculator import KeywordFrequencyCalculator
from KeywordRelevanceCalculator import KeywordRelevanceCalculator
from outgoingLinksCounter import OutgoingLinksCounter
from pageLoadTimeCalculator import PageLoadTimeCalculator
from subPageAuditor import SubPageAuditor
from videoInfoExtractor import VideoInfoExtractor

class AuditWebApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audit Web")
        
        # Initialisation des widgets d'entrée et de boutons
        self.label_url = ttk.Label(root, text="URL à auditer:")
        self.entry_url = ttk.Entry(root, width=50)
        self.label_keywords = ttk.Label(root, text="Mots-clés (séparés par des virgules):")
        self.entry_keywords = ttk.Entry(root, width=50)
        self.btn_audit = ttk.Button(root, text="Lancer l'audit", command=self.start_audit)
        self.btn_export_pdf = ttk.Button(root, text="Exporter au PDF", command=self.export_to_pdf)

        self.label_url.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_url.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        self.label_keywords.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_keywords.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        self.btn_audit.grid(row=2, column=0, padx=5, pady=5)
        self.btn_export_pdf.grid(row=2, column=1, padx=5, pady=5)

        # Création du tableau personnalisé
        self.table_frame = tk.Frame(root)
        self.table_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')
        self.columns = ["URL à auditer", "Nombre de liens sortants", "Nombre de liens entrants", "Temps de chargement de la page", "Nombre d'images détectées", "Nombre de vidéos détectées", "Nombre de balises H1", "Nombre d'images sans balise 'alt'", "keyword", "frequency"]
        self.create_custom_table()

        root.rowconfigure(3, weight=1)
        root.columnconfigure(1, weight=1)

    def start_audit(self):
        url = self.entry_url.get()
        keywords = [keyword.strip() for keyword in self.entry_keywords.get().split(',')]
        
        if not url:
            messagebox.showerror("Erreur", "Veuillez entrer une URL valide.")
            return
        
        self.clear_table()
        row = self.find_first_empty_row()
        self.audit_page(url, keywords, row)
        self.audit_sub_pages(url)

    def create_custom_table(self):
        for column in range(len(self.columns)):
            label = tk.Label(self.table_frame, text=self.columns[column], borderwidth=2, relief='groove')
            label.grid(row=0, column=column, sticky='nsew')

        # Pré-remplir quelques lignes pour la démonstration
        for row in range(1, 101):
            for column in range(len(self.columns)):
                entry = tk.Entry(self.table_frame, borderwidth=2, relief='groove')
                entry.grid(row=row, column=column, sticky='nsew', padx=1, pady=1)
                if row % 2 == 0:
                    entry.config(bg='lightgray')  # Colorer chaque seconde ligne pour une meilleure lisibilité

    def audit_sub_pages(self, main_url):
        sub_page_auditor = SubPageAuditor(main_url)
        sub_page_auditor.start()
        sub_page_auditor.join()
        sub_pages = sub_page_auditor.sub_pages
        for sub_page in sub_pages:
            row = self.find_first_empty_row()
            self.audit_page(sub_page, [], row)

    def audit_page(self, url, keywords, row):
        html_fetcher = HTMLFetcher(url)
        html_fetcher.start()
        html_fetcher.join()
        html = html_fetcher.html

        if html:
            outgoing_links_counter = OutgoingLinksCounter(html)
            incoming_links_counter = IncomingLinksCounter(html, url)
            page_load_time_calculator = PageLoadTimeCalculator(url)
            image_info_extractor = ImageInfoExtractor(html)
            video_info_extractor = VideoInfoExtractor(html)
            h1_tags_extractor = H1TagsExtractor(html)
            alt_tags_checker = AltTagsChecker(html)
            keyword_frequency_calculator = KeywordFrequencyCalculator(html, keywords)

            threads = [
                outgoing_links_counter,
                incoming_links_counter,
                page_load_time_calculator,
                image_info_extractor,
                video_info_extractor,
                h1_tags_extractor,
                alt_tags_checker,
                keyword_frequency_calculator,
            ]

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()

            keyword_relevance_calculator = KeywordRelevanceCalculator(keyword_frequency_calculator.keyword_frequency)
            keyword_relevance_calculator.start()
            keyword_relevance_calculator.join()

            # Collecter les résultats
            data = [
                url, 
                outgoing_links_counter.outgoing_links, 
                incoming_links_counter.incoming_links, 
                f"{page_load_time_calculator.load_time:.2f}s", 
                len(image_info_extractor.images_info), 
                len(video_info_extractor.videos_info), 
                "OK" if h1_tags_extractor.h1_tags else "NOK", 
                alt_tags_checker.missing_alt_count,
                ', '.join(keywords),
                keyword_relevance_calculator.keyword_relevance 
            ]
            self.display_results(data, row)
            self.root.update()

    def display_results(self, data, row):
        for col, value in enumerate(data):
            # Conditions for setting text color
            if col == 6 and value == "OK":
                fg_color = "green"
            elif col in [1, 2, 4, 5, 7] and value == 0:
                fg_color = "red"
            elif col == 6 and value == "NOK":
                fg_color = "red"
            else:
                fg_color = "black"

            self.set_cell_value(row, col, str(value), fg=fg_color)


    def set_cell_value(self, row, column, value, fg="black", bg="white"):
        entry = self.get_table_entry(row, column)
        if entry:
            entry.delete(0, tk.END)
            entry.insert(0, value)
            entry.config(fg=fg, bg=bg)

    def get_table_entry(self, row, column):
        for widget in self.table_frame.winfo_children():
            if isinstance(widget, tk.Entry) and widget.grid_info()['row'] == row and widget.grid_info()['column'] == column:
                return widget
        return None
    
    def clear_table(self):
        # Parcourir tous les widgets Entry dans table_frame et les effacer
        for widget in self.table_frame.winfo_children():
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)

    def find_first_empty_row(self):
        row_count = self.table_frame.grid_size()[1]  # Nombre de lignes actuelles dans le tableau
        for row in range(1, row_count + 1):  # +1 car range est exclusif à la fin
            if all(self.get_table_entry(row, col).get() == "" for col in range(len(self.columns)) if self.get_table_entry(row, col) is not None):
                return row
        # Si toutes les lignes existantes sont remplies, retournez la prochaine ligne disponible
        return row_count + 1


    def export_to_pdf(self):
        filename = "audit_web_results.pdf"
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Ajouter l'en-tête du document
        pdf.cell(200, 10, txt="Résultats de l'audit web", ln=True, align="C")
        pdf.ln(20)

        for row in range(1, self.find_first_empty_row()):
            url = self.get_table_entry(row, 0).get() if self.get_table_entry(row, 0) else ""
            h1_status = self.get_table_entry(row, 6).get() if self.get_table_entry(row, 6) else ""
            alt_tags = self.get_table_entry(row, 7).get() if self.get_table_entry(row, 7) else ""

            # Ajouter le lien audité
            pdf.set_font("Arial", 'B', size=12)
            pdf.cell(200, 10, txt=f"Lien audité: {url}", ln=True)
            pdf.set_font("Arial", size=12)
            pdf.ln(5)

            # Ajouter les détails et les recommandations
            recommendations = []
            if h1_status == "NOK":
                recommendations.append("Ajoutez des balises H1 pour améliorer la structure et le SEO.")
            if alt_tags == "0":
                recommendations.append("Ajoutez des attributs alt aux images pour améliorer l'accessibilité et le SEO.")

            for recommendation in recommendations:
                pdf.set_text_color(255, 0, 0)  # Couleur rouge pour les recommandations
                pdf.cell(200, 10, txt=recommendation, ln=True)
                pdf.ln(5)

            pdf.set_text_color(0, 0, 0)  # Retour à la couleur noire
            pdf.ln(10)

        pdf.output(filename)
        messagebox.showinfo("Export PDF", f"Le fichier PDF '{filename}' a été généré avec succès.")


if __name__ == "__main__":
    root = tk.Tk()
    app = AuditWebApp(root)
    root.mainloop() 