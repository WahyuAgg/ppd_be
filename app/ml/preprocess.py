import re

def clean_text(text: str):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "URL", text)
    text = re.sub(r"@\w+", "USER", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    return text

def extract_numeric_features(raw: str):
    char_count = len(raw)
    word_count = len(raw.split())
    capital_count = len([w for w in raw.split() if w.isupper() and len(w) > 1])
    exclamation_count = raw.count("!")
    return [[char_count, word_count, capital_count, exclamation_count]]
