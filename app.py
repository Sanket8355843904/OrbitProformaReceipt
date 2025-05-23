import streamlit as st
from docx import Document
from datetime import date
from io import BytesIO
from tempfile import NamedTemporaryFile
import os
import platform

# Only Windows/macOS support docx2pdf
if platform.system() not in ("Windows", "Darwin"):
    st.error("❌ PDF generation with docx2pdf only works on Windows or macOS.")
    st.stop()

from docx2pdf import convert

TEMPLATE_PATH = "template.docx"

def generate_filled_docx(data):
    doc = Document(TEMPLATE_PATH)
    for p in doc.paragraphs:
        for key, value in data.items():
            if key in p.text:
                for run in p.runs:
                    run.text = run.text.replace(key, value)
    temp_docx = NamedTemporaryFile(delete=False, suffix=".docx")
    doc.save(temp_docx.name)
    return temp_docx.name

def convert_docx_to_pdf(docx_path):
    temp_pdf = NamedTemporaryFile(delete=False, suffix=".pdf")
    convert(docx_path, temp_pdf.name)
    return temp_pdf.name

# Streamlit UI
st.set_page_config(page_title="Proforma Receipt Generator", layout="centered")
st.title("🚜 Proforma Receipt Generator")
st.caption("For Higher Orbit Agritech Pvt. Ltd.")

with st.form("receipt_form"):
    st.subheader("Receipt Information")
    receipt_suffix = st.text_input("Receipt Number (last 3 digits)", "001")
    receipt_no = f"ORBIT/2025/1/{receipt_suffix.zfill(3)}"
    receipt_date = st.date_input("Receipt Date", date.today())

    st.subheader("Customer Details")
    customer_name = st.text_input("Customer Name")
    address = st.text_area("Address")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email (optional)", "")

    st.subheader("Payment Details")
    amount_received = st.text_input("Amount Received (₹)")
    payment_mode = st.selectbox("Payment Mode", ["Cashfree", "Cash", "Other"])
    reference_id = st.text_input("Reference ID (optional)", "")
    payment_date = st.date_input("Payment Date", date.today())

    st.subheader("Booking Details")
    balance_amount = st.text_input("Balance Amount (₹)")
    tentative_delivery = st.date_input("Tentative Delivery Date", date.today())

    submitted = st.form_submit_button("Generate Receipt")

if submitted:
    placeholder_map = {
        "____________": receipt_suffix.zfill(3),
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

    filled_docx_path = generate_filled_docx(placeholder_map)
    pdf_path = convert_docx_to_pdf(filled_docx_path)

    with open(pdf_path, "rb") as f:
        st.success("✅ PDF receipt generated successfully!")
        st.download_button(
            label="📄 Download Receipt (PDF)",
            data=f,
            file_name=f"Receipt_{receipt_suffix.zfill(3)}.pdf",
            mime="application/pdf"
        )

    # Cleanup temp files
    os.remove(filled_docx_path)
    os.remove(pdf_path)
