import string
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

# Download the necessary NLTK data.
nltk.download('stopwords')

# Combine Turkish and English stopwords.
stop_words_tr = set(stopwords.words('turkish'))
stop_words_en = set(stopwords.words('english'))
stop_words = stop_words_tr.union(stop_words_en)

# The email undergoing preprocessing.
def preprocess(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = text.split()
    tokens = [word for word in tokens if word not in stop_words and len(word) > 2]
    return ' '.join(tokens)

# TF-IDF vectorizer section
def extract_important_keywords(text, top_n=10):
    processed_text = preprocess(text)
    if not processed_text:
        return ""

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([processed_text])
    feature_names = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.toarray()[0]

    word_scores = list(zip(feature_names, scores))
    sorted_words = sorted(word_scores, key=lambda x: x[1], reverse=True)
    
    keywords = [word for word, score in sorted_words[:top_n]]
    
    return " ".join(keywords)