import os, json, streamlit as st
from dotenv import load_dotenv
from pipeline import run_pipeline
# from utils.documents import read_uploaded_file

load_dotenv()
st.set_page_config(page_title="VerifyMate AI", page_icon="🔎", layout="wide")
st.title("🔎 VerifyMate AI")
st.caption("Multi-Agent Information Verification & Conflict Detection")

with st.sidebar:
    st.header("Agent Workflow")
    st.write("1. Extract claims")
    st.write("2. Compare sources")
    st.write("3. Detect conflicts")
    st.write("4. Verify evidence")
    st.write("5. Generate report")

uploads = st.file_uploader(
    "Upload 2 or more sources",
    type=["pdf", "txt", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploads:
    st.write(f"**{len(uploads)} source(s) uploaded**")
    for f in uploads:
        st.info(f.name)

    if st.button("🚀 Verify Information", type="primary"):
        if len(uploads) < 2:
            st.error("Upload at least 2 sources.")
        elif not os.getenv("GEMINI_API_KEY"):
            st.error("Add GEMINI_API_KEY to your .env file.")
        else:
            with st.status("Running VerifyMate agents...", expanded=True) as status:
                sources = [{"name": f.name, "text": f.getvalue().decode("utf-8")} for f in uploads]
                result = run_pipeline(sources)
                status.update(label="Verification complete", state="complete")
            st.session_state["result"] = result

if "result" in st.session_state:
    r = st.session_state["result"]
    claims = r.get("claims", [])
    conflicts = r.get("conflicts", [])
    unclear = r.get("unclear", [])
    consistent = r.get("consistent", [])

    st.divider()
    st.subheader("📊 Verification Overview")
    a,b,c,d = st.columns(4)
    a.metric("Claims Found", len(claims))
    b.metric("Consistent", len(consistent))
    c.metric("Conflicts", len(conflicts))
    d.metric("Unclear", len(unclear))

    st.subheader("🔴 Conflicts Detected")
    if conflicts:
        for x in conflicts:
            with st.expander(x.get("claim", "Conflict")):
                st.write(x.get("explanation", ""))
                for e in x.get("evidence", []):
                    st.markdown(f"- **{e.get('source','Source')}**: {e.get('text','')}")
    else:
        st.success("No direct conflicts detected.")

    st.subheader("🟡 Unclear / Needs Verification")
    for x in unclear:
        st.warning(x.get("claim", "Unclear claim"))
        st.write(x.get("reason", ""))

    st.subheader("🟢 Consistent Information")
    for x in consistent:
        st.write("✓ " + x.get("claim", ""))
        for e in x.get("evidence", []):
            st.caption(f"{e.get('source','Source')}: {e.get('text','')}")

    st.subheader("🧾 Final Report")
    st.write(r.get("summary", ""))

    st.download_button(
        "Download JSON Report",
        json.dumps(r, indent=2),
        "verifymate_report.json",
        "application/json"
    )
else:
    st.info("Demo tip: use the sample documents included in the project.")
