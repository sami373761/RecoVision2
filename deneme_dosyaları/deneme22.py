import joblib

# Kayıtlı modeli ve vectorizer'ı yükle
clf = joblib.load("saved_model3.pkl")
vectorizer = joblib.load("vectorizer3.pkl")

# Yeni cümlelerde tahmin yapalım
new_sentences = [
    ""
    "I love watching movies on weekends.",
    "The cinematography in that film was stunning.",
    "Can you recommend a good thriller?",
    "Give me"
]


new_sentences_vectorized = vectorizer.transform(new_sentences)
predictions_proba = clf.predict_proba(new_sentences_vectorized)[:, 1]
predictions = (predictions_proba > 0.8).astype(int)  # Karar eşiği 0.8 yapıldı

for sentence, label in zip(new_sentences, predictions):
    if label == 0:
        label = " "
    elif label == 1:
        label = "CATEGORY"
    print(f"{sentence} =>  {label}")
