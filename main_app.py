import streamlit as st
from src.intelligence import get_dossier

st.set_page_config(page_title="Trustpair Strategist", layout="wide")
st.title("💼 Trustpair Enterprise AE Strategist")

ticker = st.text_input("Enter Ticker (e.g., NVDA):").upper()
name = st.text_input("Enter Company Name:")

if st.button("Generate Strategy"):
    if ticker and name:
        with st.spinner("Analyzing signals with industry benchmarks..."):
            try:
                # Calls the logic from the src/intelligence.py module
                dossier = get_dossier(ticker, name)
                st.markdown(dossier)
            except Exception as e:
                st.error(f"Analysis error: {e}")
    else:
        st.warning("Please enter both a ticker and a company name.")