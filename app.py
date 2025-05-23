import streamlit as st
from docx import Document
from datetime import date
from io import BytesIO

TEMPLATE_PATH = "Sales Advance Receipt Template.docx"

def generate_filled_docx(data, template_path=TEMPLATE_PATH):
    doc = Document(template_path)
    
    # Clear all paragraphs (optional) or comment this if you want to keep template text
    # for para in doc.paragraphs:
    #     p = para._element
    #     p.getparent().remove(p)
    
    # Append your data as paragraphs
    doc.add_paragraph("Proforma Receipt\n")
    doc.add_paragraph(f"Receipt No: {data['receipt_no']}\t\tDate: {data['receipt_date']}\n")
    doc.add_paragraph(f"Customer Name: {data['customer_name']}")
    doc.add_paragraph(f"Address: {data['address']}")
    doc.add_paragraph(f"Phone Number: {data['phone']}")
    doc.add_paragraph(f"Email: {data['email']}")
    doc.add_paragraph(f"Amount Received: ₹ {data['amount_received']} /-")
    doc.add_paragraph(f"Payment Mode: {data['payment_mode']}")
    doc.add_paragraph(f"Reference ID: {data['reference_id']}")
    doc.add_paragraph(f"Date of Payment: {data['payment_date']}")
    doc.add_paragraph(f"Balance Amount: ₹ {data['balance_amount']} /-")
    doc.add_paragraph(f"Tentative Delivery Date: {data['tentative_delivery']}")
    doc.add_paragraph("\nAcknowledgement:\nWe acknowledge receipt of the above-mentioned amount as advance towards booking of the Orbit PT Pro. This receipt confirms the reservation of your machine. The final invoice will be issued at the time of full payment and delivery.")
    doc.add_paragraph("\nAuthorised Signatory\n")
    doc.add_paragraph("For Higher Orbit Agritech Pvt. Ltd.\nGST: 27AAHCH1976Q1ZS")

    doc_stream = BytesIO()
    doc.save(doc_stream)
    doc_stream.seek(0)
    return doc_stream

st.title("Proforma Receipt Generator - Append Text")

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
    data = {
        "receipt_no": receipt_no,
        "receipt_date": receipt_date.strftime("%d/%m/%Y"),
        "customer_name": customer_name,
        "address": address,
        "phone": phone,
        "email": email or "N/A",
        "amount_received": amount_received,
        "payment_mode": payment_mode,
        "reference_id": reference_id or "N/A",
        "payment_date": payment_date.strftime("%d/%m/%Y"),
        "balance_amount": balance_amount,
        "tentative_delivery": tentative_delivery.strftime("%d/%m/%Y"),
    }

    filled_docx = generate_filled_docx(data)

    st.success("✅ Word document generated successfully!")
    st.download_button(
        label="📄 Download Receipt (DOCX)",
        data=filled_docx,
        file_name=f"Receipt_{receipt_no.replace('/', '_')}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
