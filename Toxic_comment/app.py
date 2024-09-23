### Importing the required packages
import streamlit as st
import joblib
import numpy as np
import pandas as pd
import os
import re

# Load the vectorizer
try:
    vec = joblib.load("model/vectorizer.pkl")
except FileNotFoundError:
    st.error("Vectorizer file not found. Please ensure 'model/vectorizer.pkl' is available.")
    st.stop()

# Load models and 'r' values
label_cols = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
models = {}
rs = {}

for label in label_cols:
    model_file = f'model/model_{label}.pkl'
    if os.path.exists(model_file):
        model, r = joblib.load(model_file)
        models[label] = model
        rs[label] = r
    else:
        st.error(f"Model file for '{label}' not found. Please ensure '{model_file}' is available.")
        st.stop()

# Define the tokenize function
def tokenize(text):
    tokens = re.findall(r'\b\w+\b', text.lower())
    return tokens

# Define Streamlit app
def main():
    st.title('Toxic Comment Classifier')
    st.write('Enter a comment below to check its toxicity levels.')

    # Text input
    comment = st.text_area('Comment', height=150)

    if st.button('Check Toxicity'):
        if comment.strip() == '':
            st.warning("Please enter a comment to analyze.")
        else:
            # Preprocess the comment
            comment_vec = vec.transform([comment])
            predictions = {}

            for label in label_cols:
                r = rs[label]
                model = models[label]
                comment_nb = comment_vec.multiply(r)
                proba = model.predict_proba(comment_nb)[:, 1][0]
                predictions[label] = round(proba * 100, 2)

            st.subheader("Results:")
            for label, proba in predictions.items():
                st.write(f"**{label.capitalize()}**: {proba}%")

            # Display a bar chart
            st.subheader("Toxicity Levels")
            chart_data = pd.DataFrame({
                'Label': predictions.keys(),
                'Probability': predictions.values()
            })
            chart_data.set_index('Label', inplace=True)
            st.bar_chart(chart_data)

if __name__ == '__main__':
    main()
