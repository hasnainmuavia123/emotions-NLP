# -*- coding: utf-8 -*-
"""Emotion Detection.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1cbZwez2ZALsxzjU230eWBxJqiQnmkLC4
"""

import pandas as pd
import string
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import wordnet
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Download necessary NLTK datasets
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

# Load your dataset
df = pd.read_csv('/content/English Emotion dataset.csv')

df.head()

df["Emotion"].value_counts()

df.info()

df.columns

df = df.drop(columns=['Unnamed: 0'])

df.head(10)

import seaborn as sns
import matplotlib.pyplot as plt

sns.countplot(x='Emotion', data=df)
plt.title('Class Distribution (Emotion Categories)')
plt.show()

from wordcloud import WordCloud

emotions = df['Emotion'].unique()
for emotion in emotions:
    words = ' '.join(df[df['Emotion'] == emotion]['Subtitle'])
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(words)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(f'Word Cloud for {emotion.capitalize()}')
    plt.axis('off')
    plt.show()

import string

def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation))

df['Subtitle'] = df['Subtitle'].apply(remove_punctuation)

import re

def remove_urls(text):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub(r'', text)

df['Subtitle'] = df['Subtitle'].apply(remove_urls)

from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

def remove_stopwords(text):
    return " ".join([word for word in text.split() if word.lower() not in stop_words])

df['Subtitle'] = df['Subtitle'].apply(remove_stopwords)

def lowercase_text(text):
    return text.lower()

df['Subtitle'] = df['Subtitle'].apply(lowercase_text)

from nltk.tokenize import word_tokenize

def tokenize_text(text):
    return word_tokenize(text)

df['Subtitle'] = df['Subtitle'].apply(tokenize_text)

from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

def stem_text(text):
    return [stemmer.stem(word) for word in text]

df['Subtitle'] = df['Subtitle'].apply(stem_text)

from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import nltk

lemmatizer = WordNetLemmatizer()

def get_wordnet_pos(word):
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ, "N": wordnet.NOUN, "V": wordnet.VERB, "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)

def lemmatize_text(text):
    return [lemmatizer.lemmatize(word, get_wordnet_pos(word)) for word in text]

df['Subtitle'] = df['Subtitle'].apply(lemmatize_text)

def join_tokens(tokens):
    return ' '.join(tokens)

df['Subtitle'] = df['Subtitle'].apply(join_tokens)

from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(max_features=5000)
X_tfidf = tfidf.fit_transform(df['Subtitle']).toarray()
y = df['Emotion']  # Target variable

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.3, random_state=42)

from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

nb = MultinomialNB()
nb.fit(X_train, y_train)

y_pred_nb = nb.predict(X_test)
print("Naive Bayes Classification Report:\n", classification_report(y_test, y_pred_nb))
print("Naive Bayes Accuracy:", accuracy_score(y_test, y_pred_nb))

from sklearn.linear_model import LogisticRegression

log_reg = LogisticRegression()
log_reg.fit(X_train, y_train)

y_pred_log_reg = log_reg.predict(X_test)
print("Logistic Regression Classification Report:\n", classification_report(y_test, y_pred_log_reg))
print("Logistic Regression Accuracy:", accuracy_score(y_test, y_pred_log_reg))

import seaborn as sns
import matplotlib.pyplot as plt

def plot_confusion_matrix(y_true, y_pred, title, labels):
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.title(title)
    plt.show()

labels = df['Emotion'].unique()

# Naive Bayes Confusion Matrix
plot_confusion_matrix(y_test, y_pred_nb, 'Naive Bayes Confusion Matrix', labels)

# Logistic Regression Confusion Matrix
plot_confusion_matrix(y_test, y_pred_log_reg, 'Logistic Regression Confusion Matrix', labels)

pip install joblib

import joblib

# Save the Logistic Regression model
joblib.dump(log_reg, 'logistic_regression_emotion_model.pkl')

joblib.dump(tfidf, 'tfidf_vectorizer.pkl')

!pip install gradio

import gradio as gr
import joblib
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the saved model
log_reg = joblib.load('logistic_regression_emotion_model.pkl')

# Load the TF-IDF vectorizer (assuming you saved it similarly)
tfidf = joblib.load('tfidf_vectorizer.pkl')

# Function to predict emotion
def predict_emotion(text):
    processed_text = preprocess_text(text)  # Apply preprocessing
    text_vectorized = tfidf.transform([processed_text]).toarray()
    prediction = log_reg.predict(text_vectorized)[0]
    return prediction.capitalize()

# Text preprocessing function (same as used during model training)
def preprocess_text(text):
    text = remove_punctuation(text)
    text = remove_urls(text)
    text = remove_stopwords(text)
    text = lowercase_text(text)
    text = tokenize_text(text)
    text = stem_text(text)
    text = lemmatize_text(text)
    text = join_tokens(text)
    return text

# Define Gradio interface
iface = gr.Interface(
    fn=predict_emotion,
    inputs="text",
    outputs="label",
    title="Emotion Detection",
    description="Enter a sentence to predict its emotion category.",
    theme="dark",  # Set dark theme
    css=".footer {display:none !important;}"  # Hide the footer
)

# Launch the app
iface.launch()

import gradio as gr
import joblib

# Load the saved model and vectorizer
log_reg = joblib.load('logistic_regression_emotion_model.pkl')
tfidf = joblib.load('tfidf_vectorizer.pkl')

# Function to preprocess text
def preprocess_text(text):
    text = remove_punctuation(text)
    text = remove_urls(text)
    text = remove_stopwords(text)
    text = lowercase_text(text)
    text = tokenize_text(text)
    text = stem_text(text)
    text = lemmatize_text(text)
    text = join_tokens(text)
    return text

# Function to predict emotion
def predict_emotion(text):
    processed_text = preprocess_text(text)
    text_vectorized = tfidf.transform([processed_text]).toarray()
    prediction = log_reg.predict(text_vectorized)[0]
    return prediction.capitalize()

# Define Gradio interface with enhanced layout
with gr.Blocks(theme="dark") as iface:
    gr.Markdown("<h1 style='text-align: center;'>Emotion Detection App</h1>")
    gr.Markdown("<p style='text-align: center;'>Enter a sentence to predict its emotion category. This model supports emotions like sadness, anger, love, fear, joy, and neutral.</p>")
    with gr.Row():
        with gr.Column(scale=3):
            text_input = gr.Textbox(label="Enter Text", placeholder="Type your sentence here...", lines=3)
        with gr.Column(scale=1):
            emotion_output = gr.Label(label="Predicted Emotion")

    # Predict button
    btn = gr.Button("Predict Emotion")
    btn.click(fn=predict_emotion, inputs=text_input, outputs=emotion_output)

iface.launch()



