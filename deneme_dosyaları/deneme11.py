import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib  # Modeli kaydetmek ve tekrar yüklemek için

df = pd.read_csv("cleaned_data3.csv")  

X = df["sentence"]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

vectorizer = CountVectorizer()
X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)

# 1’in çıkma oranını daha da azaltmak için ayarlar sıkılaştırıldı
clf = RandomForestClassifier(random_state=42, class_weight={0: 1, 1: 6})
clf.fit(X_train_vectorized, y_train)

# MODELİ KAYDETME (BİR DAHA TRAIN ETMEMEK İÇİN)
joblib.dump(clf, "saved_model3.pkl")  # Eğitilmiş modeli kaydet
joblib.dump(vectorizer, "vectorizer3.pkl")  # Vectorizer'ı da kaydet

# Doğruluk ölçümü
y_pred_proba = clf.predict_proba(X_test_vectorized)[:, 1]
y_pred = (y_pred_proba > 0.85).astype(int)  # Karar eşiği 0.85 yapıldı

accuracy = accuracy_score(y_test, y_pred)
print(f"Model Doğruluk Oranı (Accuracy): {accuracy:.4f}")
