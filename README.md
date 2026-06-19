AE Intelligence Bot
The AE Intelligence Bot is a specialized AI-powered sales engineering tool designed for Account Executives. It automates the process of auditing potential clients by synthesizing SEC 10-K filings, industry benchmarks, and real-time market data to identify buying signals and procurement risks.

Features
Automated SEC Audits: Extracts and analyzes critical risk factors (Section 1A) from 10-K filings.

Industry Benchmarking: Integrates research to validate procurement strategies and build credible business cases.

Strategy Engine: Generates personalized "Executive Hooks" and fit scores to help Account Executives tailor their outreach.

Privacy-First: Securely manages sensitive credentials via environment-specific configuration.

Project Structure
Plaintext
/
├── main_app.py           # Streamlit entry point
├── src/
│   └── intelligence.py   # Core logic for data extraction and AI analysis
├── requirements.txt      # Python dependencies
└── .gitignore            # Security configuration
Setup & Installation
Clone the repository:

Bash
git clone https://github.com/ericmyerst-ai/AE-Intelligence-Bot.git
cd AE-Intelligence-Bot
Install dependencies:

Bash
pip install -r requirements.txt
Configure Secrets:
Create a .streamlit/secrets.toml file in the root directory:

Ini, TOML
OPENAI_API_KEY = "your-openai-key"
SEC_API_KEY = "your-sec-api-key"
TAVILY_API_KEY = "your-tavily-key"
Run the application:

Bash
streamlit run main_app.py
License
This project is for internal use for Trustpair sales engineering workflows.
