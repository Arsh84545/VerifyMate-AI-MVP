import streamlit as st
from pipeline import run_pipeline

st.set_page_config(page_title="VerifyMate AI", page_icon="🔎", layout="wide")

st.title("🔎 VerifyMate AI")
st.caption("Multi-Agent Information Verification & Conflict Detection")

st.subheader("Provide Sources for Verification")

col1, col2 = st.columns(2)

with col1:
    source1_text = st.text_area("Source 1 Text", height=150, value="The project submission deadline is 9:00 PM today.")

with col2:
    source2_text = st.text_area("Source 2 Text", height=150, value="The project submission deadline is 10:00 PM today.")

if st.button("Run Verification Pipeline", type="primary"):
    if not source1_text or not source2_text:
        st.warning("Please provide text in both sources.")
    else:
        sources = [
            {"name": "Source 1", "text": source1_text},
            {"name": "Source 2", "text": source2_text}
        ]
        
        with st.spinner("Running VerifyMate agents..."):
            try:
                result = run_pipeline(sources)
                
                st.success("Verification Completed!")
                
                tab1, tab2, tab3 = st.tabs(["Extraction", "Conflicts", "Final Report"])
                
                with tab1:
                    st.json(result.get("extraction", {}))
                
                with tab2:
                    st.json(result.get("conflicts", {}))
                
                with tab3:
                    st.markdown(result.get("report", ""))
                    
            except Exception as e:
                st.error(f"Error running pipeline: {str(e)}")
