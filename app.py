import os
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()


import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from core.appwrite_client import fetch_table_records
from core.query_engine import translate_prompt_to_appwrite_queries


load_dotenv()

st.set_page_config(page_title="QueryLens - Natural Language DB Explorer", layout="wide")

st.title("🔍 QueryLens")
st.markdown("### Inspect, query, and visualize your Appwrite databases using plain English.")

# Sidebar configuration
st.sidebar.header("Database Connection")
db_id = st.sidebar.text_input("Appwrite Database ID", value="6ae0c502000d943135f8")
collection_id = st.sidebar.text_input("Collection ID", value="6ae0c5dc0010edb0d21c")

user_prompt = st.text_input("Ask a question about your data:", placeholder="e.g., Show users from Nepal")

if st.button("Run Query"):
    with st.spinner("Analyzing prompt and querying Appwrite TablesDB..."):
        try:
            # First fetch raw records to inspect columns
            sample_docs = fetch_table_records(db_id, collection_id)
            if sample_docs:
                sample_cols = [k for k in sample_docs[0].keys() if not k.startswith("$")]
                
                # Translate natural language to Appwrite queries using LLM
                dynamic_queries = translate_prompt_to_appwrite_queries(user_prompt, sample_cols)
                
                # Fetch filtered documents
                filtered_docs = fetch_table_records(db_id, collection_id, queries=dynamic_queries)
                
                cleaned_docs = [{k: v for k, v in doc.items() if not k.startswith("$")} for doc in filtered_docs]
                df = pd.DataFrame(cleaned_docs)
                
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
                st.warning("No records found in this table.")
        except Exception as e:
            st.error(f"Error processing query: {e}")