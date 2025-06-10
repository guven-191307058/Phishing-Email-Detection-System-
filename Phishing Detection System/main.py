import schedule
import time
from email_fetcher import fetch_emails, save_to_csv ,load_last_uid,save_last_uid
from predict_label import predict_email_label 
import imaplib
import email
import os
from dotenv import load_dotenv # Fetch information in .env file
from pathlib import Path



# File path var password for security
dotenv_path = Path('C:/Users/ckazi/OneDrive/Masaüstü/Project B/password.env')
load_dotenv(dotenv_path=dotenv_path)

# Assignment opeation
GMAIL_USER = os.getenv('GMAIL_USER')
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')

# Accessing to gmail inbox
if not GMAIL_USER or not GMAIL_APP_PASSWORD:
    print("Hata: Gmail kullanıcı adı veya şifre yüklenemedi.")
    exit(1)
else:
    print("Gmail adresi ve şifre yüklendi.")

# The function responsible for checking and saving emails
def job():
    print("E-posta kontrolü başlatıldı...")

    # UID checking
    last_uid = load_last_uid("last_uid_inbox.txt")
    
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(GMAIL_USER, GMAIL_APP_PASSWORD)
    mail.select('inbox')

    # UID range starting from (last_uid + 1) onwards
    status, messages = mail.uid('search', None, f'(UID {int(last_uid) + 1}:*)')

    if status != "OK":
        print("Yeni eposta gelmedi.")
        mail.logout()
        return

    uids = [int(uid) for uid in messages[0].split()]
    max_uid = max(uids)
    

    if max_uid>last_uid:
        print(f"{len(uids)} yeni e-posta bulundu.")
        new_data = fetch_emails(GMAIL_USER, GMAIL_APP_PASSWORD, uids)

        # The save_to_csv function should return the prediction results.
        predictions = save_to_csv(new_data)

        # Print predictions to the screen.
        for sender_address, label_text in predictions:
            print(f" Gönderen: {sender_address}")
            print(f" Tahmin edilen tür: {label_text}")

        # Write the latest UID to the file
        save_last_uid("last_uid_inbox.txt", max_uid)
    else:
        print("Yeni e-posta bulunamadı.")
        mail.logout()

# With this line, the job function runs every 1 minute.
schedule.every(1).minutes.do(job)  

while True:
    schedule.run_pending()  # Runs scheduled tasks.
    time.sleep(1)  # Waits for 1 second.
