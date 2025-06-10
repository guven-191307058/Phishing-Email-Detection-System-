import joblib
import numpy as np
import re
from datetime import datetime
import csv
from email_fetcher import fetch_emails


# Load brfore prediction due to if train model may be changed or upgraded.
model = joblib.load("xgb_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

# Possible Phishing Keywords Dictionary. (It'll be used temporarily.)
phishing_keywords = [
    "güvenlik doğrulaması", "ödeme", "uyarı", "kimlik", "click link", "reset password", "kart", "urgent",
    "confirm your account", "banka hesabınız", "look at notification", "ele geçirildi","şifre yenieme", "invoice", "change password",
    "doğrulama", "tracking", "help center", "security issues", "access to link", "payment is here", "service", "acil oturum açma",
    "go to messages", "suspend", "visit website", "email vertification", "hesap doğrulaması", "look at details", "customer service sumber",
    "verify your password", "bank account", "support center", "please doing request", "check information", "onay", "credit records", "giriş",
    "transaction", "Alert","identity", "confirm account details", "tehdit", "look at notice", "login account", "click link",
    "tracking","urgent", "card","suspicious statement", "security issues", "hesabınızı güncelle"
]



# This function is for feature engineering parameters like in train_model.py .
def extract_features_single(body, sender_address, vectorizer):
    text = body
    url_count = len(re.findall(r'http[s]?://\S+', text))
    keyword_count = sum(1 for word in phishing_keywords if word in body.lower())
    text_length = len(text)
    uppercase_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
    specialchar_ratio = len(re.findall(r'[!@#$%^&*(),.?":{}|<>]', text)) / max(len(text), 1)
    has_html = int(bool(re.search(r'<[^>]+>', text)))
    domain = sender_address.split("@")[-1] if "@" in sender_address else "unknown"
    domain_encoded = hash(domain) % 1000

    tfidf_features = vectorizer.transform([text]).toarray()
    numerical_features = np.array([[url_count, keyword_count, text_length,
                                     uppercase_ratio, specialchar_ratio, has_html, domain_encoded]])
    
    combined_features = np.hstack([tfidf_features, numerical_features])
    return combined_features

# This is for double check mechanism temporarily.
def check_phishing_by_keywords(text):
    text_lower = text.lower()
    for word in phishing_keywords:
        
        if word in text_lower:
            print(f"Anahtar kelime tespit edildi: '{word}' ->Phishing")
            last_predict="phishing"
            return last_predict
        else:
            last_predict="normal"
    
    print("Phishing kelime bulunamadı ->", last_predict)
    return last_predict


# The predict is made by this function.
def predict_email_label(body, sender_address, subject=""):
    combined_text = subject + " " + body
    X = extract_features_single(body, sender_address, vectorizer)
    predicted_label = model.predict(X)[0]
    model_label = "phishing" if predicted_label == 1 else "normal"
    print(f"Model tahmini: {model_label}")

    # Performs keyword checking and returns the final prediction result.
    final_label = check_phishing_by_keywords(combined_text)
    
    print(f"Nihai etiket: {final_label}")
    return final_label
