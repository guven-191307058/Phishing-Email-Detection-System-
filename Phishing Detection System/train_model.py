import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
import xgboost as xgb
import joblib
import warnings
from bs4 import BeautifulSoup
from spellchecker import SpellChecker
from email_fetcher import get_body


warnings.filterwarnings("ignore")

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# SpellChecker İngilizce için
spell_en = SpellChecker(language='en')
# Checking spelling errors in body
def calculate_spelling_errors(text):
    # URL'leri ve noktalama işaretlerini temizleyelim
    text = re.sub(r'https?://\S+|www\.\S+', '', text)  # URL'leri kaldır
    text = re.sub(r'[^\w\s]', '', text)  # Noktalama işaretlerini temizle

    words = re.findall(r'\b\w+\b', text.lower())

    if not words:
        return 0.0

    misspelled_en = spell_en.unknown(words)
    total_misspelled = len(misspelled_en)

    return round(total_misspelled / len(words), 4)

# Combine Turkish and English stopwords.
stop_words = list(set(stopwords.words('turkish')).union(set(stopwords.words('english'))))

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




# The feature engineering section returns detailed features to be used for training purposes.
def extract_features(df):
    df = df.copy()

    # 1. HTML içeriğini temizle
    df['clean_body'] = df['body'].apply(lambda x: BeautifulSoup(str(x), 'html.parser').get_text())

    # 2. URL sayısı
    df['url_count'] = df['clean_body'].apply(lambda x: len(re.findall(r'http[s]?://\S+', str(x))))

    # 3. Kısa link sayısı
    df['short_url_count'] = df['clean_body'].apply(lambda x: len(re.findall(r'bit\.ly|tinyurl|t\.co|goo\.gl|ow\.ly', str(x))))

    # 4. Anahtar kelime sayısı
    df['keyword_count'] = df['clean_body'].apply(
         lambda x: sum(1 for word in phishing_keywords if word.lower() in str(x).lower())
    )

    # 5. E-posta uzunluğu
    df['text_length'] = df['clean_body'].apply(lambda x: len(str(x)))

    # 6. Büyük harf oranı
    df['uppercase_ratio'] = df['clean_body'].apply(lambda x: sum(1 for c in str(x) if c.isupper()) / max(len(x), 1))

    # 7. Özel karakter oranı
    df['specialchar_ratio'] = df['clean_body'].apply(lambda x: len(re.findall(r'[!@#$%^&*(),.?":{}|<>]', str(x))) / max(len(x), 1))

    # 8. Yazım hatası kontrolü
    df['random_caps_pattern'] = df['clean_body'].apply(lambda x: len(re.findall(r'[a-z][A-Z]|[A-Z]{2,}[a-z]', str(x))))

    # 9. HTML içerik var mı?
    df['has_html'] = df['body'].apply(lambda x: int(bool(re.search(r'<[^>]+>', str(x)))))

    # 10. Gönderen domain'i
    df['sender_domain'] = df['senderAddress'].apply(lambda x: x.split('@')[-1] if '@' in x else 'unknown')

    # 11. yazım hatası oranı
    df['spelling_error_ratio'] = df['body'].apply(calculate_spelling_errors)

    return df

# evaluate f1 score
def calculate_f1_score(y_true, y_pred):
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        return f1_score

# Veri seti yükleniyor
df = pd.read_csv("Final_Dataset.csv",on_bad_lines="skip")
df = extract_features(df)

# # #Etiketleri sayısal değerlere dönüştür
df['label'] = df['label'].map({'normal': 0, 'phishing': 1})

# # # # NaN etiket varsa temizle
df = df.dropna(subset=['label'])

# # # # Etiket tipini int yap
df['label'] = df['label'].astype(int)

# # # # TF-IDF özellikleri
vectorizer = TfidfVectorizer(stop_words=stop_words, max_features=3000)
tfidf_matrix = vectorizer.fit_transform(df['body'])

# # Domain'i sayısal hale getirme
df['domain_encoded'] = df['sender_domain'].astype('category').cat.codes

# Nihai özellik seti
features = np.hstack([ 
      tfidf_matrix.toarray(),
      df[['url_count', 'keyword_count', 'text_length', 'uppercase_ratio', 'specialchar_ratio', 'has_html', 'domain_encoded']].values
   ])

X = features
y = df['label']

# # Eğitim ve test bölünmesi
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,stratify=y,shuffle=True)


# # Model oluştur ve eğit
model = xgb.XGBClassifier(
       n_estimators=500,
       learning_rate=0.05,
       eval_metric='logloss',
       random_state=42
   )
model.fit(
    X_train,
    y_train,
    eval_set=[(X_test, y_test)],
    verbose=0
)

# Tahmin
y_pred = model.predict(X_test)

# Performans
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")

print("Classification Report:")
print(classification_report(y_test, y_pred))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))



# F1 skorunu hesapla
try:
    f1 = calculate_f1_score(y_test, y_pred)
except NameError:
    from sklearn.metrics import f1_score
    f1 = f1_score(y_test, y_pred)
print(f"F1 Skoru: {f1:.4f}")

# Yazım hatası oranı göster (isteğe bağlı)
if 'body' in df.columns and 'calculate_spelling_errors' in globals():
    # 'body' boş olmayan satırlardan son 5 tanesini alıyoruz
    emails = df[df['body'].notna()]['body'].tail(5).reset_index(drop=True)
    
    # Yazım hatası oranlarını hesapla
    hata_oranlari = emails.apply(calculate_spelling_errors)
    
    print("Yazım hata oranları (son 5 e-posta için):")
    print(hata_oranlari)
    
# Model ve encoder kaydet
joblib.dump(model, 'xgb_model.pkl')
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')
