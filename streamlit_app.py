import os
import streamlit as st
from ingestion import ingest_document, list_collections, delete_collection
from sla_architect import generate_sla_from_form
from analytics import ask_question_and_maybe_act

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.set_page_config(page_title="SLA Manager", layout="wide")
st.title("SLA Manager — Architect + Analyst (MVP)")

col1, col2 = st.columns([1,2])

# --- SLA Architect ---
with col1:
    st.header("SLA Architect")
    with st.form("sla_form"):
        svc_name = st.text_input("Service name","Acme Cloud DB")
        uptime = st.text_input("Guaranteed uptime (%)","99.95")
        response_time = st.text_input("Response time P1 (hrs)","1")
        penalty = st.text_input("Penalty per hour","$500")
        compliance = st.multiselect("Compliance standards",["GDPR","HIPAA","ISO27001"])
        extra_notes = st.text_area("Extra clauses")
        submitted = st.form_submit_button("Generate SLA")

    if submitted:
        sla_text = generate_sla_from_form(svc_name, uptime, response_time, penalty, compliance, extra_notes)
        st.text_area("Generated SLA", sla_text, height=300)
        if st.button("Ingest SLA"):
            tmp_path = os.path.join(UPLOAD_DIR,f"{svc_name.replace(' ','_')}.txt")
            with open(tmp_path,"w",encoding="utf-8") as f:
                f.write(sla_text)
            ingest_document(tmp_path, collection_name=svc_name.replace(' ','_'))
            st.success(f"Ingested as collection {svc_name.replace(' ','_')}")

    st.markdown("---")
    st.header("Upload SLA")
    uploaded_file = st.file_uploader("Upload SLA (PDF/TXT/DOCX)", type=["pdf","txt","docx"])
    if uploaded_file:
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(file_path,"wb") as f:
            f.write(uploaded_file.getbuffer())
        col_name = uploaded_file.name.replace(".","_")
        ingest_document(file_path, collection_name=col_name)
        st.success(f"Ingested collection {col_name}")

    st.markdown("---")
    st.header("Collections")
    collections = list_collections()
    st.write(collections)
    rem = st.text_input("Delete collection (exact name)")
    if st.button("Delete collection"):
        if rem and delete_collection(rem):
            st.success(f"Deleted {rem}")

# --- SLA Analyst ---
with col2:
    st.header("SLA Analyst")
    collections = list_collections()
    if collections:
        col_select = st.selectbox("Select collection", collections)
        question = st.text_area("Ask a question")
        if st.button("Ask"):
            if question.strip():
                result = ask_question_and_maybe_act(col_select, question)
                st.subheader("Answer")
                st.write(result["answer"])
                if result.get("ticket_created"):
                    st.success("Ticket created")
                    st.json(result["ticket"])
            else:
                st.warning("Type a question first.")
    else:
        st.info("No collections found. Generate or upload SLA first.")
