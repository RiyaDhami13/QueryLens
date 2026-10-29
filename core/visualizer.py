import streamlit as st
import pandas as pd

def render_visualizations(data):
    if not data:
        st.info("No records found to visualize.")
        return
    
    # Convert records to a Pandas DataFrame
    df = pd.DataFrame(data)
    
    st.markdown("### 📊 Data Inspector")
    st.dataframe(df, use_container_width=True)
    
    # Summary Metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Rows", len(df))
    with col2:
        st.metric("Total Columns", len(df.columns))
        
    # Basic auto-charting if numeric columns exist
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    if numeric_cols:
        st.markdown("### 📈 Quick Visualizer")
        selected_col = st.selectbox("Select numeric column to chart:", numeric_cols)
        st.bar_chart(df[selected_col])