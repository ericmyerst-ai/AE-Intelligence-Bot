import streamlit as st
from openai import OpenAI
from sec_api import QueryApi, ExtractorApi
from tavily import TavilyClient

def get_clients():
    return (
        OpenAI(api_key=st.secrets["OPENAI_API_KEY"]),
        QueryApi(api_key=st.secrets["SEC_API_KEY"]),
        ExtractorApi(api_key=st.secrets["SEC_API_KEY"]),
        TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])
    )

def get_dossier(ticker, company_name):
    client, queryApi, extractorApi, tavily_client = get_clients()
    
    # 1. Fetch SEC 10-K
    query = {"query": f'ticker:"{ticker}" AND formType:"10-K"', "size": "1"}
    filings = queryApi.get_filings(query)
    sec_data = "No SEC data found."
    if isinstance(filings, dict) and 'filings' in filings:
        filings_list = filings.get('filings', [])
        if isinstance(filings_list, list) and len(filings_list) > 0:
            url = filings_list[0].get("linkToFilingDetails")
            full_sec = extractorApi.get_section(url, "1A", "text")
            sec_data = str(full_sec)[:15000] if full_sec else "No data extracted."

    # 2. Fetch News + Research Benchmarks
    search_query = (f"'{company_name}' procurement digital transformation, "
                    f"CFO strategy, ERP migration, payment fraud risk, "
                    f"Association for Finance Professionals payment fraud statistics 2026, "
                    f"Gartner procurement benchmark data 2026")
    news = tavily_client.search(query=search_query, search_depth="advanced")
    news_text = "\n".join([f"{n['title']}: {n['content']}" for n in news.get("results", [])])[:5000]

    # 3. Generate Strategy with mandatory citations
    prompt = f"""
    Act as a Senior Sales Engineer. Audit {company_name} ({ticker}) for procurement friction.
    
    REQUIREMENT: You must cite industry research (e.g., AFP, Gartner, Deloitte) to validate your points.
    
    SEC Risk Factors: {sec_data}
    Research Intel: {news_text}

    Identify:
    1. Buying Signals: Leadership changes, ERP/CAPEX initiatives.
    2. Procurement Risk: Vulnerabilities (decentralized AP, manual processes).
    3. Trustpair Strategy: Executive hook + Fit Score (1-10). 
    
    Include a 'References' section at the end of your response with the sources used.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o", 
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content