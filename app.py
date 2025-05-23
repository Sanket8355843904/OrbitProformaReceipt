import streamlit as st
from docxtpl import DocxTemplate
from datetime import datetime

TEMPLATE_PATH = "Sales Advance Receipt Template.docx"

st.title("Proforma Receipt Generator")

def numeric_input(label, max_length, key=None):
    val = st.text_input(label, key=key)
    val = ''.join(filter(str.isdigit, val))[:max_length]
    return val

# Receipt Number (numeric, max 4 digits)
st.markdown("**Receipt Number (max 4 digits, numeric only):**")
receipt_no = numeric_input("", max_length=4, key="receipt_no")

st.markdown("**Date:**")
date = st.date_input("", datetime.today(), key="date").strftime("%d/%m/%Y")

st.markdown("**Customer Name (max 50 chars):**")
customer_name = st.text_input("", max_chars=50, key="customer_name")

st.markdown("**Address Line 1 (max 100 chars):**")
address_line1 = st.text_input("", max_chars=100, key="address_line1")

st.markdown("**Address Line 2 (max 100 chars, optional):**")
address_line2 = st.text_input("", max_chars=100, key="address_line2")

st.markdown("**Phone Number (max 10 digits, numeric only):**")
phone = numeric_input("", max_length=10, key="phone")

st.markdown("**Email (optional, max 50 chars):**")
email = st.text_input("", max_chars=50, key="email")

st.markdown("**Amount Received (₹) (max 10 chars, numeric only):**")
amount_received = st.text_input("", max_chars=10, key="amount_received")

st.markdown("**Payment Mode:**")
payment_mode = st.selectbox("", ["Cashfree", "Cash", "Other"], key="payment_mode")

st.markdown("**Reference ID (optional, max 20 chars, numeric only):**")
reference_id = st.text_input("", max_chars=20, key="reference_id")

st.markdown("**Date of Payment:**")
payment_date = st.date_input("", datetime.today(), key="payment_date").strftime("%d/%m/%Y")

st.markdown("**Balance Amount Due (₹) (max 10 chars, numeric only):**")
balance_due = st.text_input("", max_chars=10, key="balance_due")

st.markdown("**Tentative Delivery Date:**")
tentative_delivery = st.date_input("", datetime.today(), key="tentative_delivery").strftime("%d/%m/%Y")

if st.button("Generate Receipt DOCX"):
    if not receipt_no:
        st.error("Receipt Number is required and must be numeric up to 4 digits.")
    elif len(phone) != 10:
        st.error("Phone Number must be exactly 10 digits.")
    else:
        doc = DocxTemplate(TEMPLATE_PATH)

        # Prepare context and skip address_line2 if empty
        context = {
            "receipt_no": receipt_no,
            "date": date,
            "customer_name": customer_name,
            "address_line1": address_line1,
            "phone": phone,
            "email": email if email else "N/A",
            "amount_received": amount_received,
            "payment_mode": payment_mode,
            "reference_id": reference_id if reference_id else "N/A",
            "payment_date": payment_date,
            "balance_due": balance_due,
            "tentative_delivery": tentative_delivery,
        }

        # Only add address_line2 if it is not empty
        if address_line2.strip():
            context["address_line2"] = address_line2
        else:
            # If you want to avoid empty lines in the doc, 
            # remove or handle it in your template accordingly.
            context["address_line2"] = ""

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
