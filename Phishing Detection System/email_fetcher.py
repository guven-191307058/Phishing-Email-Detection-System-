import imaplib
import email
from email.utils import parseaddr
import os
from dotenv import load_dotenv
from pathlib import Path
import csv
import re
from important_keywords import extract_important_keywords
import joblib
import numpy as np
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer



# File path var password for security.
dotenv_path = Path('C:/Users/ckazi/OneDrive/Masaüstü/Project B/password.env')
load_dotenv(dotenv_path=dotenv_path)

# Assignment opeation.
GMAIL_USER = os.getenv('GMAIL_USER')
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')

# Accessing to gmail inbox.
if not GMAIL_USER or not GMAIL_APP_PASSWORD:
    print("Hata: Gmail kullanıcı adı veya şifresi .env dosyasından alınamadı.")
    exit(1)
else:
    print("Gmail adresi ve şifre yüklendi.")

# The email body is extracted.
def get_body(msg):
    
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                return part.get_payload(decode=True).decode(errors="ignore")
    else:
        return msg.get_payload(decode=True).decode(errors="ignore")

# Extracts URLs from the email.
def extract_urls(text):
    
    url_pattern = r"https?://[^\s<>\"']+|www\.[^\s<>\"']+"
    return re.findall(url_pattern, text)

# Fecth last UID value.
def load_last_uid(dosya=""):
    try:
        with open(dosya, "r") as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0

# Save last UID value.
def save_last_uid(path,uid):
    with open(path, "w") as f:
        f.write(str(uid))

# This function is charge of fetching emails.        
def fetch_emails(GMAIL_USER, GMAIL_APP_PASSWORD, uid_list):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(GMAIL_USER, GMAIL_APP_PASSWORD)
    mail.select('inbox', 'readonly')  # If the second folder like 'spam' is not applicable here, it should be removed.

    email_data = []

    for uid in uid_list:
        try:
            result, msg_data = mail.uid('fetch', str(uid), '(RFC822)')
            if result != 'OK':
                print(f"UID {uid} alınamadı. Sonuç: {result}")
                continue

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = msg['subject']
                    sender = msg['from']
                    body = get_body(msg)
                    sender_name, sender_email = parseaddr(sender)

                    if sender_email == GMAIL_USER:
                        continue

                    important_keywords = extract_important_keywords(body)
                    urls = extract_urls(body)

                    email_data.append({
                        "sender": sender_name,
                        "senderAddress": sender_email,
                        "subject": subject,
                        "body": body,
                        "important_keywords": important_keywords,
                        "url": urls
                    })

        except Exception as e:
            print(f"UID {uid} işlenemedi: {e}")

    mail.logout()
    return email_data





from predict_label import predict_email_label 

# Clean HTML Tags in emails.
def clean_html(raw_html):
   
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text(separator=" ", strip=True)
# This function limits the text to 100 characters.
def truncate_text(text, max_len=100):
    
    if len(text) > max_len:
        return text[:max_len] + "..."
    return text

# This function saves emails to .csv file
def save_to_csv(email_data, filename='Final_Dataset.csv'):
    import re
    from bs4 import BeautifulSoup
    import os
    import csv

    file_exists = os.path.isfile(filename)
    fieldnames = ["sender", "senderAddress", "subject", "body", "url", "label"]
    predictions = []

    def clean_and_trim(text, max_words=50):
        if not text:
            return ""
        text = BeautifulSoup(text, "html.parser").get_text()
        
        text = re.sub(r'[^a-zA-Z\s]', '', text)

        text = text.replace("\n", " ").replace("\r", " ")
  
        words = text.strip().split()
        
        return " ".join(words[:max_words])
    
    def filter_urls(url_list, max_length=25):
        
        return [url for url in url_list if len(url) <= max_length]

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)

        if not file_exists:
            writer.writeheader()

        for email in email_data:
            predicted_label = predict_email_label(
                email.get("body", ""),
                email.get("senderAddress", ""),
                email.get("subject", "")
            )

            label_text = predicted_label 
            predictions.append((email.get("senderAddress",), label_text))

            writer.writerow({
                "sender": email.get("sender", ""),
                "senderAddress": email.get("senderAddress", ""),
                "subject": clean_and_trim(email.get("subject", ""), max_words=50),
                "body": clean_and_trim(email.get("body", ""), max_words=50),
                "url": " ".join([u for u in email.get("url", []) if len(u) <= 25]),
                "label": predict_email_label(
                    email.get("body", ""),
                    email.get("senderAddress", ""),
                    email.get("Subject", "")
                    )
            })

    return predictions



