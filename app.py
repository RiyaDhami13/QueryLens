import os
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from core.appwrite_client import fetch_table_records
from core.query_engine import translate_prompt_to_appwrite_queries

load_dotenv()

st.set_page_config(page_title="QueryLens - Natural Language DB Explorer", layout="wide")

st.title("🔍 QueryLens")
st.markdown("### Inspect, query, and visualize your Appwrite databases using plain English.")

# Sidebar configuration
st.sidebar.markdown("### 🗂️ Data Source")

data_source_option = st.sidebar.radio(
    "Select Source:",
    ["Appwrite Database", "Upload Custom CSV / XLSX"]
)

df_source = None
uploaded_file = None

if data_source_option == "Upload Custom CSV / XLSX":
    uploaded_file = st.sidebar.file_uploader("Upload your spreadsheet", type=["csv", "xlsx"])
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            df_source = pd.read_csv(uploaded_file)
        else:
            df_source = pd.read_excel(uploaded_file)
        st.sidebar.success(f"Loaded {uploaded_file.name} successfully!")
    else:
        st.sidebar.info("Please upload a CSV or XLSX file to begin.")
else:
    st.sidebar.markdown("### Database Connection")
    db_id = st.sidebar.text_input(
        "Appwrite Database ID", 
        value="6ae0c502000d943135f8", 
        key="appwrite_db_id_input"
    )
    collection_id = st.sidebar.text_input(
        "Collection ID", 
        value="6ae0c5dc0010edb0d21c", 
        key="appwrite_collection_id_input"
    )

user_prompt = st.text_input("Ask a question about your data:", placeholder="e.g., num > 600000 or Hyde Park")

if st.button("Run Query"):
    with st.spinner("Analyzing prompt and querying data source..."):
        try:
            if data_source_option == "Upload Custom CSV / XLSX":
                if uploaded_file is None or df_source is None:
                    st.warning("Please upload a CSV or XLSX file first.")
                    st.stop()
                
                df = df_source.copy()
                if user_prompt:
                    prompt_lower = user_prompt.lower()
                    import re
                    # Detect numeric comparisons like 'num > 600000'
                    match_comp = re.search(r'([a-zA-Z_]\w*)\s*(>|<|>=|<=|==|=)\s*([0-9.]+)', prompt_lower)
                    if match_comp:
                        col, op, val = match_comp.groups()
                        val = float(val) if '.' in val else int(val)
                        # Find matching column case-insensitively
                        matching_cols = [c for c in df.columns if c.lower() == col.lower()]
                        if matching_cols:
                            actual_col = matching_cols[0]
                            if op == '>':
                                df = df[df[actual_col] > val]
                            elif op == '<':
                                df = df[df[actual_col] < val]
                            elif op in ['==', '=']:
                                df = df[df[actual_col] == val]
                            elif op == '>=':
                                df = df[actual_col] >= val
                            elif op == '<=':
                                df = df[actual_col] <= val
                    else:
                        # Fallback to text search
                        mask = df.astype(str).apply(lambda x: x.str.lower().str.contains(prompt_lower)).any(axis=1)
                        df = df[mask]
            else:
                # Appwrite / Mock database logic
                sample_docs = fetch_table_records(db_id, collection_id)
                if sample_docs:
                    sample_cols = [k for k in sample_docs[0].keys() if not k.startswith("$")]
                    dynamic_queries = translate_prompt_to_appwrite_queries(user_prompt, sample_cols)
                    filtered_docs = fetch_table_records(db_id, collection_id, queries=dynamic_queries, prompt=user_prompt)
                    cleaned_docs = [{k: v for k, v in doc.items() if not k.startswith("$")} for doc in filtered_docs]
                    df = pd.DataFrame(cleaned_docs)
                else:
                    df = pd.DataFrame()
                    
            if not df.empty:
                st.success(f"Query executed! Found {len(df)} matching records.")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("📊 Interactive Table View")
                    st.dataframe(df, use_container_width=True)
                    
                with col2:
                    st.subheader("📈 Auto-Generated Visualization")
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    text_cols = df.select_dtypes(include=['object']).columns
                    if len(numeric_cols) > 0 and len(text_cols) > 0:
                        st.bar_chart(df.set_index(text_cols[0])[numeric_cols[0]])
                    else:
                        st.info("Chart will appear when numerical data is present.")
                        
                st.download_button("📥 Export Results as CSV", data=df.to_csv(index=False), file_name="querylens_export.csv", mime="text/csv")
            else:
                st.warning("No records found matching your query.")
                
        except Exception as e:
            st.error(f"Error processing query: {e}")