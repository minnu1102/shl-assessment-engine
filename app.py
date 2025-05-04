
import streamlit as st
import pandas as pd
import json
from src.recommendation_engine import RecommendationEngine
from src.evaluation import calculate_metrics

# Initialize the recommendation engine
engine = RecommendationEngine()

st.set_page_config(
    page_title="SHL Assessment Navigator",
    page_icon="📊",
    layout="wide"
)

st.title("SHL Assessment Navigator")
st.write("Find the perfect assessments for your hiring needs")

# Sidebar for metrics
with st.sidebar:
    st.header("System Evaluation")
    
    # Load metrics
    try:
        with open('data/evaluation_results.json', 'r') as f:
            metrics = json.load(f)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Recall@3", f"{metrics['recallAt3']*100:.1f}%")
        with col2:
            st.metric("MAP@3", f"{metrics['mapAt3']*100:.1f}%")
        
        st.caption("These metrics are calculated based on our benchmark test dataset.")
    except:
        st.warning("Evaluation metrics not available. Run evaluation to generate metrics.")
        if st.button("Run Evaluation"):
            with st.spinner("Calculating metrics..."):
                metrics = calculate_metrics()
                st.success("Evaluation completed!")
                st.experimental_rerun()

# Main content
st.header("Search for Assessments")

# Search form
query = st.text_area(
    "Enter Job Description or Query",
    placeholder="Paste job description or enter a search query (e.g., 'Software Developer position requiring strong analytical skills and programming experience')",
    height=150
)

col1, col2 = st.columns([3, 1])
with col2:
    max_results = st.selectbox("Max Results", [3, 5, 10], index=1)

if st.button("Find Assessments", type="primary", disabled=not query.strip()):
    if not query.strip():
        st.warning("Please enter a search query.")
    else:
        with st.spinner("Searching for assessments..."):
            results = engine.get_recommendations(query, max_results)
            
        if not results:
            st.info("No matching assessments found. Try modifying your search query.")
        else:
            st.success(f"Found {len(results)} matching assessments.")
            
            # Display results in a table
            df = pd.DataFrame(results)
            
            # Apply formatting
            df['Remote Testing'] = df['remoteTestingSupport'].apply(lambda x: "✅" if x else "❌")
            df['Adaptive/IRT'] = df['adaptiveSupport'].apply(lambda x: "✅" if x else "❌")
            
            # Reorder and select columns for display
            display_df = df[['name', 'testType', 'duration', 'Remote Testing', 'Adaptive/IRT', 'description']]
            display_df.columns = ['Assessment', 'Type', 'Duration', 'Remote Testing', 'Adaptive/IRT', 'Description']
            
            st.dataframe(
                display_df,
                column_config={
                    "Assessment": st.column_config.LinkColumn(),
                    "Description": st.column_config.TextColumn(width="large"),
                },
                hide_index=True,
            )

# API Documentation
st.header("API Documentation")
with st.expander("View API Documentation"):
    st.code("""
    # Health Check
    GET /api/health
    
    # Recommendations
    POST /api/recommend
    {
      "query": "Software Developer with Python skills",
      "maxResults": 5
    }
    """)
    st.write("The API is available at `http://localhost:8000` when running the API server.")
    st.caption("Run `python -m src.api.main` to start the API server.")

# Footer
st.markdown("---")
st.caption("SHL Assessment Navigator © 2023 | Powered by AI-based matching technology")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

