import pandas as pd
import joblib
import re
import string
import math
from collections import Counter

def extract_entropy_details(text):
    if not text:
        return 0.0, 0.0, 0.0, 0.0, 0.0

    total_len = len(text)
    freq = Counter(text)
    entropy = -sum((count / total_len) * math.log2(count / total_len) for count in freq.values())

    non_ascii_count = sum(1 for c in text if ord(c) > 127)
    digit_count = sum(1 for c in text if c.isdigit())
    punct_count = sum(1 for c in text if c in string.punctuation)

    entropy_per_char = entropy / total_len if total_len > 0 else 0.0
    percent_non_ascii = non_ascii_count / total_len
    percent_digits = digit_count / total_len
    percent_punct = punct_count / total_len

    return entropy, entropy_per_char, percent_non_ascii, percent_digits, percent_punct

def extract_features(df):
    df = df.copy()

    df['subject_len'] = df['subject'].str.len()
    df['num_words_subject'] = df['subject'].str.split().str.len()
    df['body_len'] = df['body'].str.len()
    df['num_words_body'] = df['body'].str.split().str.len()
    df['subject_density'] = df['subject_len'] / (df['num_words_subject'] + 1)
    df['body_density'] = df['body_len'] / (df['num_words_body'] + 1)
    df['num_exclamations'] = df['body'].str.count(r'!')

    entropy_details = df['body'].apply(extract_entropy_details)
    df['body_entropy'] = entropy_details.apply(lambda x: round(x[0], 4))
    df['body_entropy_per_char'] = entropy_details.apply(lambda x: round(x[1], 6))
    df['percent_digits'] = entropy_details.apply(lambda x: round(x[3], 4))
    df['percent_punct'] = entropy_details.apply(lambda x: round(x[4], 4))

    df['text'] = df['subject'] + ' ' + df['body']

    # Rimuovi colonne non utilizzate nel modello
    df = df.drop(columns=[
        'num_words_body', 'num_words_subject',
    ])

    return df

def predict_spam(subject, body, model_path='predicter/spam_classifier_pipeline.joblib'):

    data = pd.DataFrame([{'subject': subject, 'body': body}])

    features = extract_features(data)

    model = joblib.load(model_path)

    prediction = model.predict(features)[0]
    spam_proba = model.predict_proba(features)[0][1]

    has_url = bool(re.search(r'http[s]?://', body))

    reasons = []

    if bool(prediction) is True:
        reasons = classify_spam_reason(subject, body)

    return {
        'is_spam': bool(prediction),
        'spam_probability': round(spam_proba, 2),
        'spam_reasons': reasons,
        'contains_url': has_url
    }

def classify_spam_reason(subject, body):
    text = (subject + ' ' + body).lower()
    reasons = ['spam']

    if re.search(r'\b(bank|account|iban|card|login|password|verify|otp|credentials)\b', text):
        reasons.append('Dati sensibili')
    if re.search(r'http[s]?://', text):
        reasons.append('Contiene link')
    if re.search(r'http[s]?://\d{1,3}(?:\.\d{1,3}){3}', text):
        reasons.append('Link a indirizzo IP')
    if re.search(r'http[s]?://(?:bit\.ly|tinyurl\.com|freehosting)', text):
        reasons.append('Dominio sospetto')
    if re.search(r'\b(gratis|free|win|bitcoin|investment|only today|money|discount)\b', text):
        reasons.append('Marketing aggressivo')

    return reasons if reasons else ['Nessuna causa specifica identificata']