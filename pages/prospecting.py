import streamlit as st
import sys
import os

# Ensure the root directory is in the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import prospect_intelligence as intel

st.title("🔍 Trustpair Market Discovery")

region = st.text_input("Region (e.g., North America):")
industry = st.text_input("Industry Vertical (e.g., Retail):")

if st.button("Identify & Qualify Top 5 Prospects"):
    with st.spinner("Scanning market and verifying SEC revenue..."):
        prospects = intel.get_prospect_list(region, industry)
        
        for company in prospects:
            ticker = intel.get_company_ticker(company)
            revenue = intel.get_company_revenue(ticker)
            
            with st.expander(f"Potential Prospect: {company} (Ticker: {ticker})"):
                st.write(f"**Annual Revenue (Latest):** {revenue}")
                fit_analysis = intel.analyze_fit(company)
                st.write(fit_analysis)