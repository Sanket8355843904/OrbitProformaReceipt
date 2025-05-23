import streamlit as st
from docx import Document
import re
from io import BytesIO
from datetime import datetime

TEMPLATE_PATH = "Sales Advance Receipt Template.docx"

# Extract placeholder lengths
def extract_placeholders_with_limits(docx_file):
    doc = Document(docx_file)
    limits = {}
    for para in doc.paragraphs:
        matches = re.findall(r'(_{3,})', para.text)
        for match in matches:
            limits[match] = len(match)
    return limits

# Replace placeholders
def generate_receipt(template_file, data):
    doc = Document(template_file)

    replacements = {
        '____________': data['receipt_no'],
        '__/__/____': data['date'],
        '_____________________________________________________________': data['customer_name'],
        '____________________________________________________________________': data['address_line1'],
        '___________________________________________________________________________': data['address_line2'],
        '____________________________________________________________': data['phone'],
        '___________________________________________________________': data['email'],
        '__________________': data['amount_received'],
        '_________________________': data['balance_due'],
    }

    for para in doc.paragraphs:
        for key, value in replacements.items():
            if key in para.text:
                for run in para.runs:
                    run.text = run.text.replace(key, value)

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# Streamlit UI
st.set_page_config(page_title="Orbit Proforma Invoice Generator", page_icon="🧾")
st.title("🚜 Orbit Proforma Invoice Generator")

limits = extract_placeholders_with_limits(TEMPLATE_PATH)

st.subheader("Enter Receipt Details")

# Form inputs with length limits
receipt_no = st.text_input("Receipt No", max_chars=limits.get('____________', 20))
date = st.text_input("Date [DD/MM/YYYY]", value=datetime.today().strftime('%d/%m/%Y'), max_chars=limits.get('__/__/____', 10))
customer_name = st.text_input("Customer Name", max_chars=limits.get('_____________________________________________________________', 75))
address_line1 = st.text_input("Address Line 1", max_chars=limits.get('____________________________________________________________________', 80))
address_line2 = st.text_input("Address Line 2", max_chars=limits.get('___________________________________________________________________________', 80))
phone = st.text_input("Phone Number", max_chars=limits.get('____________________________________________________________', 60))
email = st.text_input("Email", max_chars=limits.get('___________________________________________________________', 60))
amount_received = st.text_input("Amount Received (₹)", max_chars=limits.get('__________________', 20))
balance_due = st.text_input("Balance Amount Due (₹)", max_chars=limits.get('_________________________', 25))

if st.button("Generate Receipt"):
    data = {
        'receipt_no': receipt_no,
        'date': date,
        'customer_name': customer_name,
        'address_line1': address_line1,
        'address_line2': address_line2,
        'phone': phone,
        'email': email,
        'amount_received': amount_received,
        'balance_due': balance_due
    }
    docx_buffer = generate_receipt(TEMPLATE_PATH, data)

    st.success("✅ Receipt Generated!")
    st.download_button("📥 Download Receipt", docx_buffer, file_name="Proforma_Receipt.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
