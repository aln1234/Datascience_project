import streamlit as st
import pickle  # Replacing joblib with pickle
import numpy as np
import pandas as pd
import os
import re
import string  # Add this import

# Re-define the tokenize function
re_tok = re.compile(f'([{string.punctuation}“”¨«»®´·º½¾¿¡§£₤‘’])')
def tokenize(s):
    return re_tok.sub(r'\1', s).split()

# Load the vectorizer
try:
    with open("model/vectorizer.pkl", "rb") as f:
        vec = pickle.load(f)
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
        with open(model_file, "rb") as f:
            model, r = pickle.load(f)
        models[label] = model
        rs[label] = r
    else:
        st.error(f"Model file for '{label}' not found. Please ensure '{model
