import streamlit as st
from docxtpl import DocxTemplate
from datetime import datetime

# Path to your .docx template
TEMPLATE_PATH = "Sales Advance Receipt Template.docx"

st.title("Sales Advance Receipt Generator")

# Inputs from user
receipt_no = st.text_input("Receipt Number")
date = st.date_input("Date", datetime.today()).strftime("%d/%m/%Y")
customer_name = st.text_input("Customer Name")
address_line1 = st.text_input("Address Line 1")
address_line2 = st.text_input("Address Line 2")
phone = st.text_input("Phone Number")
email = st.text_input("Email (optional)")
amount_received = st.text_input("Amount Received (₹)")
payment_mode = st.selectbox("Payment Mode", ["Cashfree", "Cash", "Other"])
reference_id = st.text_input("Reference ID (optional)")
payment_date = st.date_input("Date of Payment", datetime.today()).strftime("%d/%m/%Y")
balance_due = st.text_input("Balance Amount Due (₹)")
tentative_delivery = st.date_input("Tentative Delivery Date", datetime.today()).strftime("%d/%m/%Y")

if st.button("Generate Receipt DOCX"):
    # Load the template
    doc = DocxTemplate(TEMPLATE_PATH)

    # Context for template placeholders
    context = {
        "receipt_no": receipt_no,
        "date": date,
        "customer_name": customer_name,
        "address_line1": address_line1,
        "address_line2": address_line2,
        "phone": phone,
        "email": email if email else "N/A",
        "amount_received": amount_received,
        "payment_mode": payment_mode,
        "reference_id": reference_id if reference_id else "N/A",
        "payment_date": payment_date,
        "balance_due": balance_due,
        "tentative_delivery": tentative_delivery,
    }

    # Render the docx with context
    doc.render(context)

    # Save the generated receipt with a unique name
    output_filename = f"Sales_Advance_Receipt_{receipt_no}.docx"
    doc.save(output_filename)

    st.success(f"Receipt generated: {output_filename}")

    # Provide a download link
    with open(output_filename, "rb") as file:
        btn = st.download_button(
            label="Download Receipt DOCX",
            data=file,
            file_name=output_filename,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
