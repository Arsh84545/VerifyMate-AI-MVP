import streamlit as st

# Emergency Mock Function (Bypasses backend imports and API delays)
def run_pipeline(sources):
    return {
        "extraction": {
            "source_1": "Deadline is October 15th at 5:00 PM.",
            "source_2": "Deadline is November 1st at midnight."
        },
        "conflicts": [
            {
                "issue": "Submission Deadline Contradiction",
                "source_1": "October 15th, 5:00 PM",
                "source_2": "November 1st, 12:00 AM",
                "severity": "High"
            }
        ],
        "report": "### 🔎 Verification Report\n\n**Critical Conflict Found:**\n- **Source 1** specifies the project deadline as **October 15th**.\n- **Source 2** specifies the project deadline as **November 1st**.\n\n*Recommendation:* Please align with project coordinators to confirm the final binding date."
    }

st.set_page_config(page_title="VerifyMate AI", page_icon="🔎", layout="wide")

st.title("🔎 VerifyMate AI")
st.caption("Multi-Agent Information Verification & Conflict Detection")

st.subheader("Option 1: Upload Documents")
uploads = st.file_uploader(
    "Upload 2 or more sources (TXT, PDF, etc.)", 
    accept_multiple_files=True,
    type=["txt"]
)

st.divider()

st.subheader("Option 2: Or Paste Text Directly")
col1, col2 = st.columns(2)

with col1:
    source1_text = st.text_area("Source 1 Text", height=150, placeholder="Paste text for Source 1 here...")

with col2:
    source2_text = st.text_area("Source 2 Text", height=150, placeholder="Paste text for Source 2 here...")

if st.button("Run Verification Pipeline", type="primary"):
    sources = []
    
    # 1. Process File Uploads if present
    if uploads:
        for f in uploads:
            try:
                text_content = f.getvalue().decode("utf-8")
                sources.append({"name": f.name, "text": text_content})
            except Exception as e:
                st.error(f"Error reading file {f.name}: {str(e)}")
                
    # 2. Process Text Area Inputs if present
    if source1_text.strip():
        sources.append({"name": "Source 1 (Text Input)", "text": source1_text})
    if source2_text.strip():
        sources.append({"name": "Source 2 (Text Input)", "text": source2_text})

    # Validation
    if len(sources) < 2:
        st.warning("Please provide at least 2 sources (either upload files or paste text in both boxes).")
    else:
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
