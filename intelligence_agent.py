import os
import streamlit as st
from dotenv import load_dotenv
from sec_api import QueryApi, ExtractorApi
from openai import OpenAI

# 1. Configuration
load_dotenv()
SEC_API_KEY = os.getenv("SEC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

queryApi = QueryApi(api_key=SEC_API_KEY)
extractorApi = ExtractorApi(api_key=SEC_API_KEY)
client = OpenAI(api_key=OPENAI_API_KEY)

# 2. Universal Data Parser
def extract_filing_url(data):
    """Recursively search for a dictionary containing the filing URL."""
    if isinstance(data, dict):
        if 'linkToFilingDetails' in data:
            return data['linkToFilingDetails']
        for val in data.values():
            result = extract_filing_url(val)
            if result: return result
    elif isinstance(data, list):
        for item in data:
            result = extract_filing_url(item)
            if result: return result
    return None

def get_risk_intelligence(ticker):
    try:
        query = {
            "query": f"ticker:{ticker} AND formType:\"10-K\"",
            "from": "0",
            "size": "1",
            "sort": [{"filedAt": {"order": "desc"}}]
        }
        response = queryApi.get_filings(query)
        
        # Extract URL using the universal search
        url = extract_filing_url(response)
        
        if not url:
            return f"Could not find URL. Response structure: {type(response)}"
        
        # Extract Risk Factors section
        risk_factors = extractorApi.get_section(url, "1A", "text")
        return {"url": url, "content": risk_factors[:10000]} # Increased limit for better analysis
            
    except Exception as e:
        return f"Error: {str(e)}"

# 3. Streamlit UI
st.set_page_config(page_title="Trustpair Intelligence Agent", layout="wide")
st.title("🎯 Trustpair SEC Intelligence Agent")
ticker = st.text_input("Enter Company Ticker (e.g., MSFT):")

if st.button("Generate Verified Brief"):
    if ticker:
        with st.spinner("Analyzing SEC filings and aligning with Trustpair..."):
            data = get_risk_intelligence(ticker.upper())
            
            if isinstance(data, dict):
                # AI Analysis with Trustpair Alignment
                # Enhanced Prompt for AE Intelligence
                prompt = f"""
                Analyze these SEC 10-K Risk Factors: {data['content']}
                
                Your task: Act as an elite Sales Engineer. Create an intelligence briefing for an Enterprise Account Executive targeting this company.
                
                Trustpair Context:
                - Payment Fraud Prevention
                - Financial Data Integrity
                - Treasury Efficiency
                
                Structure:
                1. Prospect Fit Score (1-10): How critical is Trustpair to this company based on their SEC risks? (Justify with one sentence).
                2. Executive Briefing: High-impact summary of risks.
                3. The "Trustpair Bridge": Explicitly connect identified risks to Trustpair. 
                   e.g., "They mentioned [Risk X]; Trustpair mitigates this by [Feature Y]."
                4. Immediate Outreach Email: A 3-sentence, professional email to the CFO or Treasurer 
                   leveraging this specific risk insight. Keep it punchy and consultative.
                """
                
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}]
                )
                
                st.markdown("### 📊 Verified Strategic Intelligence")
                st.write(response.choices[0].message.content)
            else:
                st.error(data)
