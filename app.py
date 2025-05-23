import streamlit as st
from docx import Document
from datetime import date
from io import BytesIO

TEMPLATE_PATH = "Sales Advance Receipt Template.docx"

def generate_filled_docx(data):
    doc = Document(TEMPLATE_PATH)
    for p in doc.paragraphs:
        for key, value in data.items():
            if key in p.text:
                inline = p.runs
                for i in range(len(inline)):
                    if key in inline[i].text:
                        inline[i].text = inline[i].text.replace(key, value)
    # Save to a BytesIO stream instead of a temp file
    doc_stream = BytesIO()
    doc.save(doc_stream)
    doc_stream.seek(0)
    return doc_stream

st.title("🚜 Proforma Receipt Generator (Word Doc)")

with st.form("receipt_form"):
    receipt_no = st.text_input("Receipt No", "ORBIT/2025/1/001")
    receipt_date = st.date_input("Receipt Date", date.today())

    customer_name = st.text_input("Customer Name")
    address = st.text_area("Address")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email (optional)", "")

    amount_received = st.text_input("Amount Received (₹)")
    payment_mode = st.selectbox("Payment Mode", ["Cashfree", "Cash", "Other"])
    reference_id = st.text_input("Reference ID (optional)", "")
    payment_date = st.date_input("Payment Date", date.today())

    balance_amount = st.text_input("Balance Amount (₹)")
    tentative_delivery = st.date_input("Tentative Delivery Date", date.today())

    submitted = st.form_submit_button("Generate Receipt (DOCX)")

if submitted:
    placeholder_map = {
        "____________": receipt_no.split("/")[-1],
        "___/___/____": receipt_date.strftime("%d/%m/%Y"),
        "_____________________________________________________________": customer_name,
        "__________________________________________________________________": address,
        "____________________________________________________________": phone,
        "___________________________________________________________": email or "N/A",
        "₹ _______________ /-": f"₹ {amount_received} /-",
        "Cashfree / Cash / Other": payment_mode,
        "Reference ID (if available):": f"Reference ID (if available): {reference_id or 'N/A'}",
        "Date of Payment [DD/MM/YYYY]: __ /__ /____": f"Date of Payment [DD/MM/YYYY]: {payment_date.strftime('%d/%m/%Y')}",
        "₹ _____________________ /-": f"₹ {balance_amount} /-",
        "Tentative delivery date [DD/MM/YYYY]: ___ /___ /____": f"Tentative delivery date [DD/MM/YYYY]: {tentative_delivery.strftime('%d/%m/%Y')}",
    }

    filled_docx = generate_filled_docx(placeholder_map)

    st.success("✅ Word document generated successfully!")
    st.download_button(
        label="📄 Download Receipt (DOCX)",
        data=filled_docx,
        file_name=f"Receipt_{receipt_no.replace('/', '_')}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
