import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from io import BytesIO
import datetime

# Function to create PDF in-memory and return bytes
def create_pdf(data, letterhead_path):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Draw letterhead image at the top
    if letterhead_path:
        letterhead = ImageReader(letterhead_path)
        c.drawImage(letterhead, 0, height - 5*cm, width=width, height=5*cm, preserveAspectRatio=True)

    # Starting y position below letterhead
    y = height - 6*cm

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, y, "Proforma Receipt")
    y -= 1.5*cm

    # Customer Info
    c.setFont("Helvetica", 12)
    c.drawString(2*cm, y, f"Customer Name: {data['customer_name']}")
    y -= 0.8*cm
    c.drawString(2*cm, y, f"Customer Address: {data['customer_address']}")
    y -= 0.8*cm
    c.drawString(2*cm, y, f"Contact Number: {data['contact_number']}")
    y -= 1*cm

    # Receipt Details
    c.drawString(2*cm, y, f"Invoice Number: {data['invoice_number']}")
    y -= 0.8*cm
    c.drawString(2*cm, y, f"Date: {data['date']}")
    y -= 1*cm

    # Product/Service Details Table header
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2*cm, y, "Description")
    c.drawString(10*cm, y, "Quantity")
    c.drawString(13*cm, y, "Unit Price")
    c.drawString(16*cm, y, "Amount")
    y -= 0.5*cm
    c.line(2*cm, y, 19*cm, y)
    y -= 0.5*cm

    # Product rows
    c.setFont("Helvetica", 12)
    for item in data['items']:
        c.drawString(2*cm, y, item['description'])
        c.drawString(10*cm, y, str(item['quantity']))
        c.drawString(13*cm, y, f"{item['unit_price']:.2f}")
        c.drawString(16*cm, y, f"{item['amount']:.2f}")
        y -= 0.7*cm

    y -= 0.3*cm
    c.line(2*cm, y, 19*cm, y)
    y -= 0.5*cm

    # Total Amount
    c.setFont("Helvetica-Bold", 12)
    c.drawString(13*cm, y, "Total Amount:")
    c.drawString(16*cm, y, f"{data['total_amount']:.2f}")
    y -= 2*cm

    # Blank Signature Space
    c.setFont("Helvetica", 12)
    c.drawString(2*cm, y, "Authorized Signature:")
    c.rect(5*cm, y - 1*cm, 6*cm, 2*cm)  # Blank box for signature

    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(width/2, 1.5*cm, "Higher Orbit Agritech Pvt Ltd - Proforma Receipt")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# Streamlit UI
st.title("Proforma Receipt Generator")

# Input form
with st.form("receipt_form"):
    st.header("Customer Details")
    customer_name = st.text_input("Customer Name")
    customer_address = st.text_area("Customer Address")
    contact_number = st.text_input("Contact Number")

    st.header("Receipt Details")
    invoice_number = st.text_input("Invoice Number", value="INV-001")
    date = st.date_input("Date", value=datetime.date.today())

    st.header("Items")

    # For simplicity, allow entering 1 item; can extend to dynamic list if needed
    description = st.text_input("Item Description")
    quantity = st.number_input("Quantity", min_value=1, step=1, value=1)
    unit_price = st.number_input("Unit Price", min_value=0.0, step=0.01, format="%.2f", value=0.00)

    submitted = st.form_submit_button("Generate PDF")

if submitted:
    amount = quantity * unit_price
    total_amount = amount  # For now, single item

    data = {
        "customer_name": customer_name,
        "customer_address": customer_address,
        "contact_number": contact_number,
        "invoice_number": invoice_number,
        "date": date.strftime("%d-%m-%Y"),
        "items": [
            {
                "description": description,
                "quantity": quantity,
                "unit_price": unit_price,
                "amount": amount,
            }
        ],
        "total_amount": total_amount,
    }

    # Provide your letterhead image path here or upload via Streamlit if you want
    letterhead_path = "letterhead.png"  # Make sure this file is in the same folder or adjust path

    pdf_buffer = create_pdf(data, letterhead_path)

    st.success("PDF generated successfully!")
    st.download_button(
        label="Download Proforma Receipt PDF",
        data=pdf_buffer,
        file_name=f"proforma_receipt_{invoice_number}.pdf",
        mime="application/pdf"
    )
