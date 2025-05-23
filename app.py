import streamlit as st
from docxtpl import DocxTemplate, RichText
from datetime import datetime

TEMPLATE_PATH = "Sales Advance Receipt Template.docx"

st.title("Proforma Receipt Generator")

def numeric_input(label, max_length, key=None):
    val = st.text_input(label, key=key)
    val = ''.join(filter(str.isdigit, val))[:max_length]
    return val

# Inputs
st.markdown("**Receipt Number (max 4 digits, numeric only):**")
receipt_no = numeric_input("", max_length=4, key="receipt_no")

st.markdown("**Date:**")
date = st.date_input("", datetime.today(), key="date").strftime("%d/%m/%Y")

st.markdown("**Customer Name (max 50 chars):**")
customer_name = st.text_input("", max_chars=50, key="customer_name")

st.markdown("**Address (max 200 chars):**")
address = st.text_input("", max_chars=200, key="address")

st.markdown("**Phone Number (10 digits, numeric only):**")
phone = numeric_input("", max_length=10, key="phone")

st.markdown("**Email (optional, max 50 chars):**")
email = st.text_input("", max_chars=50, key="email")

st.markdown("**Amount Received (₹):**")
amount_received = st.text_input("", max_chars=10, key="amount_received")

st.markdown("**Payment Mode:**")
payment_mode = st.selectbox("", ["Cashfree", "Cash", "Other"], key="payment_mode")

st.markdown("**Reference ID (optional, max 20 chars):**")
reference_id = st.text_input("", max_chars=20, key="reference_id")

st.markdown("**Date of Payment:**")
payment_date = st.date_input("", datetime.today(), key="payment_date").strftime("%d/%m/%Y")

st.markdown("**Balance Due (₹):**")
balance_due = st.text_input("", max_chars=10, key="balance_due")

st.markdown("**Tentative Delivery Date:**")
tentative_delivery = st.date_input("", datetime.today(), key="tentative_delivery").strftime("%d/%m/%Y")

# Generate Document
if st.button("Generate Receipt DOCX"):
    if not receipt_no:
        st.error("Receipt Number is required and must be numeric up to 4 digits.")
    elif len(phone) != 10:
        st.error("Phone Number must be exactly 10 digits.")
    else:
        doc = DocxTemplate(TEMPLATE_PATH)

        context = {
            "receipt_no": RichText(receipt_no, bold=True),
            "date": RichText(date, bold=True),
            "customer_name": RichText(customer_name, bold=True),
            "address_line1": RichText(address, bold=True),
            "phone": RichText(phone, bold=True),
            "email": RichText(email if email else "N/A", bold=True),
            "amount_received": RichText(amount_received, bold=True),
            "payment_mode": RichText(payment_mode, bold=True),
            "reference_id": RichText(reference_id if reference_id else "N/A", bold=True),
            "payment_date": RichText(payment_date, bold=True),
            "balance_due": RichText(balance_due, bold=True),
            "tentative_delivery": RichText(tentative_delivery, bold=True),
        }

        doc.render(context)
        output_filename = f"Sales_Advance_Receipt_{receipt_no}.docx"
        doc.save(output_filename)
        st.success(f"Receipt generated: {output_filename}")

        with open(output_filename, "rb") as file:
            st.download_button(
                label="Download Receipt DOCX",
                data=file,
                file_name=output_filename,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
