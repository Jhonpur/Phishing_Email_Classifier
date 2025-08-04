from fpdf import FPDF
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
from io import BytesIO
import unicodedata
#from database import db
from app.database.crud import *
from app.database.models import *


def sanitize_text(text: str) -> str:
    """Replace special quotes and accents, normalize to ASCII."""
    text = text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    return text

class PDFReport(FPDF):
    # Custom PDF report class inheriting from FPDF
    def __init__(self, title, logo_path, format='A3', auto=True):
        super().__init__(format=format)
        self.title = title
        self.logo_path = logo_path
        self.set_auto_page_break(auto=auto, margin=30)

    # Custom header method
    def header(self):
        # Logo
        if self.logo_path and os.path.exists(self.logo_path):
            self.image(self.logo_path, 10, 8, 33)
        # Title
        self.set_font('Arial', 'B', 12)
        self.multi_cell(self.w - 2 * self.l_margin, 10, self.title, border=False, align='C')
        self.ln(10) # Add a line break after the title

    # Custom footer method
    def footer(self):
        # Page number
        self.set_y(-15)
        self.set_font('Arial', 'I', 10)
        self.multi_cell(self.w - 2 * self.l_margin, 10, f'Page {self.page_no()}', align='C')

    # Method to add text to the PDF
    def add_text(self, text):
        self.set_font("Arial", size=12)
        clean_text = sanitize_text(text)
        self.multi_cell(self.w - 2 * self.l_margin, 9, clean_text, ln=True)

        

    
    # Method to add in grasetto text to the PDF
    def add_text_grasetto(self, text):
        self.set_font("Arial", "B", 14)
        clean_text = sanitize_text(text)
        self.multi_cell(self.w - 2 * self.l_margin, 9, clean_text,ln=True) 
        

    # Method to add an image plot to the PDF
    def add_image_plot(self, fig):
        buffer = BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        # Use almost the full width of the page
        self.image(buffer, x=self.l_margin, w=self.w - 2 * self.l_margin)
        buffer.close()



#funzione che genera il report pdf 
def generate_report(db: Session, user_id: int) -> bytes:
    logo_path = r"C:\\Users\\ange.kadjafomekon\\OneDrive - AGM Solutions\\Desktop\\git_locale\\Phishing_Email_Classifier\\app\utils\\agm_solutions.png"
    """Generate a PDF report for the user."""

    """if "price_in_euros" not in df or "author" not in df or "publication_year" not in df:
        raise ValueError("DataFrame must contain 'author', 'price_in_euros', and 'publication_year' columns.")"""
    
    user = get_user_by_id(db, user_id) # ritorna l'utente

    pdf = PDFReport(title=sanitize_text(f"REPORT COMPLETO DI {user.nome}"), logo_path=logo_path)
    pdf.add_page()
    num_tot_mail_riceived = get_total_received_emails(db, user_id)
    num_tot_mail_sent = get_total_sent_emails(db, user_id)
    num_tot_mail_spam = get_total_spam_emails(db, user_id)
    num_tot_mail_read = get_total_read_emails(db, user_id)
    num_tot_mail_cancelled = get_total_cancelled_mails(db, user_id)
    num_tot_mail_not_read = get_total_non_read_emails(db, user_id)
    

    # grafico
    graph_report = graph_report_user(num_tot_mail_spam,num_tot_mail_riceived)
    graph_report_spam = graph_spam_reason_user(db, user_id)
    

    pdf.add_text_grasetto(f"NUMERO DI MAIL RICEVUTE :")
    pdf.add_text(f"{num_tot_mail_riceived} ")
    
    pdf.add_text_grasetto(f"NUMERO DI MAIL INVIATE :")
    pdf.add_text(f"{num_tot_mail_sent} ")
    
    pdf.add_text_grasetto(f"NUMERO TOTALE DI MAIL SPAM :")
    pdf.add_text(f"{num_tot_mail_spam } ")

    pdf.add_text_grasetto(f"NUMERO TOTALE DI MAIL LETTE :")
    pdf.add_text(f"{num_tot_mail_read} ")

    pdf.add_text_grasetto(f"NUMERO TOTALE DI MAIL CANCELLATE :")
    pdf.add_text(f"{num_tot_mail_cancelled} ")

    pdf.add_text_grasetto(f"NUMERO TOTALE DI MAIL NON LETTE :")
    pdf.add_text(f"{num_tot_mail_not_read} ")

      
    pdf.add_image_plot(graph_report)# Ajoute le graphique au PDF
    plt.close(graph_report)    


    pdf.add_image_plot(graph_report_spam)# Ajoute le graphique au PDF
    plt.close(graph_report_spam)

    return pdf.output(dest='S')        



#funzione per generare il grafico per il report 
def graph_report_user(num_tot_mail_spam,num_tot_mail_riceived):
    num_mail_no_spam = num_tot_mail_riceived - num_tot_mail_spam

    data = {'tipo mail': ['SPAM','NO SPAM'],
           'Quantità': [num_mail_no_spam ,num_tot_mail_spam]}
    df = pd.DataFrame(data)

    # Creare il grafico a barre
    fig, ax = plt.subplots()
    sns.barplot(data=df, x="tipo mail", y="Quantità", ax=ax)
    ax.set_title("confronto numero di mail spam e no spam ")
    ax.set_xlabel("tipo mail")
    ax.set_ylabel("Quantità")
    plt.xticks(rotation=25)
    ax.grid(True)

    return fig


#funzione per generare il grafico a torta per il report che mostra i tipi di spam
def graph_spam_reason_user(db: Session, user_id: int):
    spam =  get_spam_emails_by_user(db, user_id) # ottengo tutte le mail spam dell'utente
    spam_reasons = []
    for email in spam:
       if email.spam_reason and len(email.spam_reason) > 1:
            spam_reasons.extend(email.spam_reason)      
       elif email.spam_reason and len(email.spam_reason) == 1:
            spam_reasons.append(email.spam_reason)
       else:
           spam_reasons.append("Altro") # se non ci sono motivi di spam, aggiungo un messaggio predefinito
       #spam_reasons.extend(email.spam_reason) if email.spam_reason else None # aggiungo i motivi di spam alla lista spam_reasons

    # Contare le occorrenze di ogni motivo di spam
    reason_counts = pd.Series(spam_reasons).value_counts()

    # Creare il grafico a torta
    fig, ax = plt.subplots()
    reason_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax, startangle=90, legend=False)
    ax.set_ylabel('')  # Rimuovere l'etichetta dell'asse y
    ax.set_title('Motivi di Spam per l\'Utente')
    plt.tight_layout()  # Ottimizza il layout per evitare sovrapposizioni


    return fig