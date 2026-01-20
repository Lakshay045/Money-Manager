from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from datetime import datetime

# Create PDF
pdf_filename = "Kotak_Clean_Statement_Jan_2026.pdf"
doc = SimpleDocTemplate(pdf_filename, pagesize=A4, 
                        rightMargin=15*mm, leftMargin=15*mm,
                        topMargin=15*mm, bottomMargin=15*mm)

# Container for elements
elements = []
styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=18,
    textColor=colors.HexColor('#e31e24'),
    spaceAfter=5
)

heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=12,
    spaceAfter=10
)

normal_style = ParagraphStyle(
    'CustomNormal',
    parent=styles['Normal'],
    fontSize=9,
    spaceAfter=3
)

# Header
elements.append(Paragraph("Account Statement", title_style))
elements.append(Paragraph("01 Jan 2026 - 19 Jan 2026", heading_style))
elements.append(Spacer(1, 5*mm))

# Account holder info
info_text = """
<b>Lakshay Mittal</b><br/>
CRN 809267171<br/>
Room No 507 C<br/>
Iilm University Gulmohar Pg<br/>
Sector Knowledge Park 2<br/>
Gautam Budh Nagar - 201310<br/>
Uttar Pradesh - India
"""
elements.append(Paragraph(info_text, normal_style))
elements.append(Spacer(1, 5*mm))

# Account details table
account_details = [
    ['Account No.:', '6850175417', 'MICR:', '110485062'],
    ['Account Type:', 'Savings', 'IFSC Code:', 'KKBK0005028'],
    ['Branch:', 'Greater Noida', 'Currency:', 'INDIAN RUPEE'],
    ['Account Status:', 'Active', 'Nominee Registered:', 'Yes']
]

account_table = Table(account_details, colWidths=[35*mm, 35*mm, 35*mm, 35*mm])
account_table.setStyle(TableStyle([
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('TEXTCOLOR', (0, 0), (0, -1), colors.grey),
    ('TEXTCOLOR', (2, 0), (2, -1), colors.grey),
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
]))
elements.append(account_table)
elements.append(Spacer(1, 8*mm))

# Transaction header
elements.append(Paragraph("Savings Account Transactions", heading_style))

# Clean transactions data (NO Lakshay entries, NO failed transactions)
transactions_data = [
    ['#', 'Date', 'Description', 'Ref. No.', 'Withdrawal', 'Deposit', 'Balance']
]

# Opening balance
current_balance = 0.0

# Clean transaction list
txn_list = []
txn_counter = 0

# Add opening balance row
txn_list.append(['-', '-', 'Opening Balance', '-', '-', '-', '0.00'])

# All clean transactions with running balance calculation
raw_txns = [
    ['07 Jan 2026', 'UPI/Mukesh Yadav', 'UPI', '30.00', '-'],
    ['07 Jan 2026', 'UPI/Aarav Srivastava', 'UPI', '-', '50.00'],
    ['08 Jan 2026', 'UPI/Arnav Agencies', 'UPI', '10.00', '-'],
    ['08 Jan 2026', 'UPI/Jio Prepaid', 'UPI', '19.99', '-'],
    ['09 Jan 2026', 'UPI/Naresh Prajapati', 'UPI', '20.00', '-'],
    ['09 Jan 2026', 'UPI/Surya Convenience Store', 'UPI', '5.00', '-'],
    ['10 Jan 2026', 'UPI/Jio Prepaid', 'UPI', '350.99', '-'],
    ['10 Jan 2026', 'UPI/Arnav Agencies', 'UPI', '10.00', '-'],
    ['10 Jan 2026', 'UPI/Arnav Agencies', 'UPI', '20.00', '-'],
    ['10 Jan 2026', 'UPI/Arnav Agencies', 'UPI', '5.00', '-'],
    ['10 Jan 2026', 'UPI/Aditya Chaturvedi', 'UPI', '3.00', '-'],
    ['10 Jan 2026', 'UPI/Anshika Arora', 'UPI', '-', '10.00'],
    ['11 Jan 2026', 'UPI/Arnav Agencies', 'UPI', '5.00', '-'],
    ['11 Jan 2026', 'UPI/Arnav Agencies', 'UPI', '20.00', '-'],
    ['11 Jan 2026', 'UPI/Jio Prepaid', 'UPI', '19.99', '-'],
    ['12 Jan 2026', 'UPI/The Food Company', 'UPI', '5.00', '-'],
    ['12 Jan 2026', 'UPI/Arnav Agencies', 'UPI', '5.00', '-'],
    ['12 Jan 2026', 'UPI/Aditya Chaturvedi', 'UPI', '-', '15.00'],
    ['12 Jan 2026', 'UPI/Anshika Arora', 'UPI', '-', '1.00'],
    ['12 Jan 2026', 'UPI/Anshika Arora', 'UPI', '-', '11.00'],
    ['12 Jan 2026', 'UPI/Aditya Chaturvedi', 'UPI', '-', '122.50'],
    ['12 Jan 2026', 'UPI/Swiggy', 'UPI', '311.00', '-'],
    ['12 Jan 2026', 'UPI/Manisha', 'UPI', '-', '2,000.00'],
    ['12 Jan 2026', 'UPI/Aditya Chaturvedi', 'UPI', '-', '137.00'],
    ['13 Jan 2026', 'UPI/Naresh Prajapati', 'UPI', '20.00', '-'],
    ['13 Jan 2026', 'UPI/Gajendra Singh', 'UPI', '30.00', '-'],
    ['13 Jan 2026', 'UPI/Arnav Agencies', 'UPI', '15.00', '-'],
    ['13 Jan 2026', 'UPI/Aarav Srivastava', 'UPI', '-', '50.00'],
    ['13 Jan 2026', 'UPI/Arnav Agencies', 'UPI', '2.00', '-'],
    ['13 Jan 2026', 'UPI/Zepto', 'UPI', '110.00', '-'],
    ['13 Jan 2026', 'UPI/Aarav Srivastava', 'UPI', '-', '17.50'],
    ['13 Jan 2026', 'UPI/Aarav Srivastava', 'UPI', '-', '20.00'],
    ['14 Jan 2026', 'UPI/Arnav Agencies', 'UPI', '5.00', '-'],
    ['14 Jan 2026', 'UPI/Aarav Srivastava', 'UPI', '20.00', '-'],
    ['15 Jan 2026', 'UPI/Naresh Prajapati', 'UPI', '20.00', '-'],
    ['15 Jan 2026', 'UPI/Manoj Kumar', 'UPI', '10.00', '-'],
    ['16 Jan 2026', 'UPI/Manoj Nagar', 'UPI', '50.00', '-'],
    ['16 Jan 2026', 'UPI/Arnav Agencies', 'UPI', '5.00', '-'],
    ['16 Jan 2026', 'UPI/GG Machine', 'UPI', '35.00', '-'],
    ['16 Jan 2026', 'UPI/Aarav Srivastava', 'UPI', '-', '17.50'],
    ['16 Jan 2026', 'UPI/Aarav Srivastava', 'UPI', '17.50', '-'],
    ['17 Jan 2026', 'UPI/Amazon', 'UPI', '2,678.44', '-'],
    ['17 Jan 2026', 'UPI/Pinki Devi', 'UPI', '130.00', '-'],
    ['17 Jan 2026', 'UPI/Naresh Prajapati', 'UPI', '20.00', '-'],
    ['17 Jan 2026', 'UPI/Premkala Devi', 'UPI', '50.00', '-'],
    ['17 Jan 2026', 'UPI/Gajendra Singh', 'UPI', '30.00', '-'],
    ['17 Jan 2026', 'UPI/Jahnvi Mahawar', 'UPI', '200.00', '-'],
    ['17 Jan 2026', 'UPI/Aarav Srivastava', 'UPI', '-', '122.50'],
    ['17 Jan 2026', 'UPI/Aditya Chaturvedi', 'UPI', '-', '122.50'],
    ['17 Jan 2026', 'UPI/Aarav Srivastava', 'UPI', '-', '5.00'],
    ['17 Jan 2026', 'UPI/Rahul', 'UPI', '42.00', '-'],
    ['17 Jan 2026', 'UPI/Aarav Srivastava', 'UPI', '2,000.00', '-'],
    ['17 Jan 2026', 'UPI/Jahnvi Mahawar', 'UPI', '-', '50.00'],
    ['18 Jan 2026', 'UPI/Manish Nimodiya', 'UPI', '-', '1,000.00'],
    ['18 Jan 2026', 'UPI/Swiggy Limited', 'UPI', '208.00', '-'],
    ['18 Jan 2026', 'UPI/Navi Limited', 'UPI', '-', '17.00'],
    ['18 Jan 2026', 'UPI/Aditya Chaturvedi', 'UPI', '-', '49.69'],
    ['18 Jan 2026', 'UPI/Aditya Chaturvedi', 'UPI', '98.69', '-'],
    ['18 Jan 2026', 'UPI/Restaurant Brands Asia', 'UPI', '2.06', '-'],
    ['18 Jan 2026', 'UPI/Amazon', 'UPI', '479.00', '-'],
    ['18 Jan 2026', 'UPI/District Dining', 'UPI', '49.50', '-'],
    ['18 Jan 2026', 'UPI/District Dining', 'UPI', '97.50', '-'],
    ['18 Jan 2026', 'UPI/Zomatofood', 'UPI', '141.25', '-'],
    ['18 Jan 2026', 'UPI/Swiggy', 'UPI', '136.00', '-'],
    ['18 Jan 2026', 'UPI/Anshika Arora', 'UPI', '-', '25.00'],
    ['19 Jan 2026', 'UPI/Aarav Srivastava', 'UPI', '500.00', '-'],
    ['19 Jan 2026', 'UPI/Aarav Srivastava', 'UPI', '-', '500.00'],
    ['19 Jan 2026', 'UPI/Navi Limited', 'UPI', '-', '48.00'],
    ['19 Jan 2026', 'UPI/Aditya Chaturvedi', 'UPI', '500.00', '-'],
    ['19 Jan 2026', 'UPI/Aarav Srivastava', 'UPI', '-', '500.00'],
    ['19 Jan 2026', 'UPI/Aarav Srivastava', 'UPI', '500.00', '-'],
    ['19 Jan 2026', 'UPI/Aditya Chaturvedi', 'UPI', '-', '500.00'],
    ['19 Jan 2026', 'UPI/Aarav Srivastava', 'UPI', '-', '50.00'],
    ['19 Jan 2026', 'UPI/Aarav Srivastava', 'UPI', '20.00', '-'],
    ['19 Jan 2026', 'UPI/Navi Limited', 'UPI', '-', '6.00'],
    ['19 Jan 2026', 'UPI/Aditya Chaturvedi', 'UPI', '-', '20.00'],
    ['19 Jan 2026', 'UPI/Roppen Transpor', 'UPI', '15.00', '-'],
    ['19 Jan 2026', 'UPI/Navi Limited', 'UPI', '-', '2.00'],
    ['19 Jan 2026', 'UPI/Aditya Chaturvedi', 'UPI', '500.00', '-'],
    ['19 Jan 2026', 'UPI/Aditya Chaturvedi', 'UPI', '-', '500.00'],
    ['19 Jan 2026', 'UPI/Aditya Chaturvedi', 'UPI', '-', '24.99'],
    ['19 Jan 2026', 'UPI/Brokentusk', 'UPI', '1.00', '-'],
    ['19 Jan 2026', 'UPI/Brokentusk Tech', 'UPI', '-', '1.00'],
    ['19 Jan 2026', 'UPI/Decentro', 'UPI', '-', '0.01'],
    ['19 Jan 2026', 'IMPS/Billionbra', 'IMPS', '-', '1.00'],
    ['19 Jan 2026', 'UPI/Monu Kumar', 'UPI', '60.00', '-'],
    ['19 Jan 2026', 'UPI/Manisha', 'UPI', '-', '1.00'],
    ['19 Jan 2026', 'UPI/Manisha', 'UPI', '-', '200.00'],
    ['19 Jan 2026', 'UPI/Amazon Pay', 'UPI', '112.00', '-'],
]

# Process transactions and calculate running balance
for txn in raw_txns:
    txn_counter += 1
    date, desc, ref, withdrawal, deposit = txn
    
    # Calculate balance
    if withdrawal != '-':
        current_balance -= float(withdrawal.replace(',', ''))
    if deposit != '-':
        current_balance += float(deposit.replace(',', ''))
    
    # Format balance
    balance_str = f"{current_balance:,.2f}"
    
    txn_list.append([str(txn_counter), date, desc, ref, withdrawal, deposit, balance_str])

transactions_data.extend(txn_list)

# Create transaction table
txn_table = Table(transactions_data, 
                  colWidths=[8*mm, 20*mm, 50*mm, 30*mm, 18*mm, 18*mm, 18*mm],
                  repeatRows=1)

txn_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e31e24')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('ALIGN', (4, 0), (-1, -1), 'RIGHT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 7),
    ('FONTSIZE', (0, 1), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
]))

elements.append(txn_table)
elements.append(Spacer(1, 8*mm))

# Summary box
summary_data = [
    ['Account Summary'],
    ['Opening Balance:', '₹ 0.00'],
    ['Closing Balance:', f'₹ {current_balance:,.2f}']
]

summary_table = Table(summary_data, colWidths=[70*mm, 70*mm])
summary_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f5f5f5')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#e31e24')),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
    ('LEFTPADDING', (0, 0), (-1, -1), 10),
    ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#e31e24')),
]))

elements.append(summary_table)
elements.append(Spacer(1, 8*mm))

# Footer information
footer_text = """
<b>End of Statement</b><br/>
<br/>
Any discrepancy in the statement should be brought to the notice of Kotak Mahindra Bank Ltd. within one month from the date of receipt of the statement.<br/>
<br/>
This is a system generated report and does not require signature & stamp.<br/>
<br/>
<b>For assistance, reach out to us at:</b><br/>
📞 1860 266 0811 (local call charges apply)<br/>
<br/>
<b>Branch Address:</b><br/>
Harsha Mall Alfa-1, Commercial Belt., Greater Noida-201308, Uttar Pradesh, India<br/>
<br/>
Kotak Mahindra Bank Ltd. | CIN: L65110MH1985PLC038137<br/>
Registered Office: 27 BKC, C 27, G Block, Bandra Kurla Complex, Bandra (E), Mumbai - 400 051.<br/>
www.kotak.bank.in
"""

footer_style = ParagraphStyle(
    'Footer',
    parent=styles['Normal'],
    fontSize=7,
    textColor=colors.grey
)

elements.append(Paragraph(footer_text, footer_style))

# Build PDF
doc.build(elements)

print(f"✅ PDF successfully created: {pdf_filename}")
print(f"📄 Total Transactions: {txn_counter}")
print(f"💰 Final Balance: ₹{current_balance:,.2f}")