### importing the required packages
import streamlit as st
import joblib
import numpy as np

#load the vectorizer
try:
    vec = joblib.load("model/vectorizer.pkl")
except FileNotFoundError:
    st.error("Vectorizer file not found. Please ensure 'vectorizer.pkl' is available ")
    st.stop()