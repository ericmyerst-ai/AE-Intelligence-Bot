import streamlit as st
from pypdf import PdfReader

st.set_page_config(page_title="Core Parser", layout="centered")
st.title("📄 10-K Core Parser")

# 1. UPLOAD
uploaded_file = st.file_uploader("Upload 10-K PDF", type=["pdf"])

# 2. EXTRACTION
if uploaded_file:
    reader = PdfReader(uploaded_file)
    total_pages = len(reader.pages)
    st.write(f"Document Loaded: {total_pages} pages detected.")
    
    # Extract text from specific pages or the whole doc
    full_text = ""
    for i in range(min(total_pages, 20)): # Limit to 20 pages for stability
        full_text += reader.pages[i].extract_text() + "\n"
    
    # 3. DISPLAY
    st.subheader("Extracted Content (Preview)")
    st.text_area("Content", full_text[:5000], height=400)
    
    # Optional: Logic to find specific keywords
    if st.button("Search for 'Consolidated Statements'"):
        if "Consolidated Statements" in full_text:
            st.success("Found 'Consolidated Statements' in the document!")
        else:
            st.warning("Keyword not found in the first 20 pages.")