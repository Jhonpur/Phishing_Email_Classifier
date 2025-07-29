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

    # df['num_links'] = df['body'].str.count(r'http[s]?://')
    # df['num_special_chars'] = df['body'].str.count(r'[\$\@\!\#\%]')
    df['num_exclamations'] = df['body'].str.count(r'!')

    # df['has_ip_link'] = df['body'].str.contains(r'http[s]?://\d{1,3}(?:\.\d{1,3}){3}').astype(int)
    # df['has_bank_word'] = df['body'].str.contains(r'\b(?:bank|account|verify|login|password)\b', flags=re.IGNORECASE).astype(int)

    entropy_details = df['body'].apply(extract_entropy_details)
    df['body_entropy'] = entropy_details.apply(lambda x: round(x[0], 4))
    df['body_entropy_per_char'] = entropy_details.apply(lambda x: round(x[1], 6))
    # df['percent_non_ascii'] = entropy_details.apply(lambda x: round(x[2], 4))
    df['percent_digits'] = entropy_details.apply(lambda x: round(x[3], 4))
    df['percent_punct'] = entropy_details.apply(lambda x: round(x[4], 4))

    df['text'] = df['subject'] + ' ' + df['body']

    # Rimuovi colonne non utilizzate nel modello
    df = df.drop(columns=[
        'num_words_body', 'num_words_subject',
        # 'num_links', 'num_special_chars',
        # 'has_ip_link', 'has_bank_word',
        # 'percent_non_ascii'
    ])

    return df

def predict_spam(subject, body, model_path='spam_classifier_pipeline.joblib'):

    data = pd.DataFrame([{'subject': subject, 'body': body}])

    features = extract_features(data)

    model = joblib.load(model_path)

    prediction = model.predict(features)[0]
    spam_proba = model.predict_proba(features)[0][1]

    return {
        'is_spam': bool(prediction),
        'spam_probability': round(spam_proba, 4)
    }

# if __name__ == '__main__':
#     body = "I want to steal all your money"
#     subject = "Send me your money"
#     path = "predicter/spam_classifier_pipeline.joblib"
#     result = predict_spam(subject, body, path)
#     print(result)

#     body = "Today we have a meeting at 13:00 with teams"
#     subject = "Today's meeting"
#     path = "predicter/spam_classifier_pipeline.joblib"
#     result = predict_spam(subject, body, path)
#     print(result)