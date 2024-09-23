### importing the required packages
import streamlit as st
import joblib
import numpy as np

# Load the vectorizer
vec = joblib.load("model/vectorizer.pkl")


#load models and 'r' values
label_cols = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
models = {}
rs ={}

for label in label_cols:
    #load each model and its corresponding 'r' value
    model,r = joblib.load(f'model/model_{label}.pkl')
    models[label] = model
    rs[label] = r
    

