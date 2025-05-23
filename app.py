import streamlit as st
from docx import Document
from datetime import date
from io import BytesIO

TEMPLATE_PATH = "Sales Advance Receipt Template.docx"

def replace_placeholder(paragraph, placeholder, replacement):
    full_text = ''.join(run.text for run in paragraph.runs)
    if placeholder not in full_text:
        return
    new_text = full_text.replace(placeholder, replacement)
    for run in paragraph.runs:
        run.text = ''
    paragraph.runs[0].text = new_text

def generate_filled_docx(data, template_path=TEMPLATE_PATH):
    doc = Document(template_path)

    # Replace in paragraphs
    for paragraph in doc.paragraphs:
        for key, val in data.items():
            replace_placeholder(paragraph, key, val)

    # Replace in tables too (if needed)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for key, val in data.items():
                        replace_placeholder(paragraph, key, val)

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
        "{{receipt_no}}": receipt_no,
        "{{receipt_date}}": receipt_date.strftime("%d/%m/%Y"),
        "{{customer_name}}": customer_name,
        "{{address}}": address,
        "{{phone}}": phone,
        "{{email}}": email or "N/A",
        "{{amount_received}}": f"₹ {amount_received} /-",
        "{{payment_mode}}": payment_mode,
        "{{reference_id}}": reference_id or "N/A",
        "{{payment_date}}": payment_date.strftime("%d/%m/%Y"),
        "{{balance_amount}}": f"₹ {balance_amount} /-",
        "{{tentative_delivery}}": tentative_delivery.strftime("%d/%m/%Y"),
    }

    filled_docx = generate_filled_docx(placeholder_map)

    st.success("✅ Word document generated successfully!")
    st.download_button(
        label="📄 Download Receipt (DOCX)",
        data=filled_docx,
        file_name=f"Receipt_{receipt_no.replace('/', '_')}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
