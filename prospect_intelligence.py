import os
from tavily import TavilyClient
from openai import OpenAI
from edgar import set_identity, Company

# Initialize the clients
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# SEC identity is required
set_identity("Trustpair Prospector ericm@example.com")

def get_prospect_list(region, industry):
    """Searches for companies and extracts a clean list."""
    query = f"{industry} companies in {region} treasury procurement payment security"
    results = tavily.search(
        query=query, 
        include_domains=["linkedin.com/company"], 
        max_results=8, 
        search_depth="advanced"
    )
    
    snippets = "\n".join([f"- {r['title']}: {r['content']}" for r in results.get('results', [])])
    
    prompt = f"""
    Extract exactly 5 large enterprises (Revenue > $500M) in the {industry} sector in {region}. 
    Exclude Fintechs, TMS providers, and software platforms.
    OUTPUT FORMAT: Return ONLY the company names, one per line. No filler.
    
    Snippets:
    {snippets}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    
    raw_output = response.choices[0].message.content.strip().split('\n')
    cleaned = [line.strip().lstrip('0123456789.-* ') for line in raw_output if len(line) > 2]
    return list(set(cleaned))[:5]

def get_company_ticker(company_name):
    """Asks the LLM to identify the ticker for a company name."""
    prompt = f"What is the stock ticker symbol for {company_name}? Return ONLY the ticker symbol, nothing else."
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def get_company_revenue(ticker):
    """Safely fetches latest annual revenue by filtering for the GAAP revenue concept."""
    if not ticker or ticker.upper() in ["N/A", "NONE", "UNKNOWN"]:
        return "N/A"
        
    try:
        company = Company(ticker)
        financials = company.get_financials()
        df = financials.income_statement().to_dataframe()
        
        # Filter for the specific US-GAAP revenue concept
        revenue_row = df[df['concept'] == 'us-gaap_RevenueFromContractWithCustomerExcludingAssessedTax']
        
        if not revenue_row.empty:
            # The columns '2025-06-30 (FY)' etc., contain the values. 
            # We take the first available date column.
            latest_year_col = revenue_row.columns 
            revenue_value = revenue_row.iloc[latest_year_col]
            
            return f"${float(revenue_value):,.0f}"
        
        return "Revenue data not found"
        
    except Exception as e:
        return f"Error: {e}"

def analyze_fit(company_name):
    """Researches company and evaluates Trustpair fit."""
    search_results = tavily.search(query=f"'{company_name}' treasury procurement payment fraud risk", max_results=3)
    context = "\n".join([f"{r['content']}" for r in search_results.get('results', [])])
    
    system_instruction = "You are an expert Trustpair Sales Engineer."
    user_prompt = f"""
    Analyze this company: {company_name}
    Research Context: {context}
    Provide a Fit Score (1-10), the most likely pain point, and how Trustpair solves it.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o", 
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content