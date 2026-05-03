# app.py — Full Week 1 Version

import streamlit as st
from PIL import Image
import pytesseract
import cv2
import numpy as np
import re

# ---- FUNCTIONS ----

def preprocess_image(pil_image):
    img = np.array(pil_image)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255,
                               cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return Image.fromarray(thresh)

def extract_text(pil_image):
    processed = preprocess_image(pil_image)
    text = pytesseract.image_to_string(processed, config='--psm 6')
    return text

def parse_expense(text):
    result = {"amount": None, "date": None, "merchant": None}

    # Amount
    amount_match = re.search(
        r'₹\s*([0-9,]+(?:\.[0-9]{1,2})?)|Rs\.?\s*([0-9,]+)',
        text, re.IGNORECASE)
    if amount_match:
        amt = (amount_match.group(1) or amount_match.group(2)).replace(',','')
        result["amount"] = float(amt)

    # Date
    date_match = re.search(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', text)
    if date_match:
        result["date"] = date_match.group(0)

    # Merchant (known list)
    known = {'swiggy':'Swiggy','zomato':'Zomato','amazon':'Amazon',
             'uber':'Uber','ola':'Ola','netflix':'Netflix',
             'bigbasket':'BigBasket','flipkart':'Flipkart'}
    for k, v in known.items():
        if k in text.lower():
            result["merchant"] = v
            break

    return result

# ---- UI ----

st.set_page_config(page_title="💰 Expense Extractor", page_icon="💰")
st.title("💰 Financial Advisor — Week 1")
st.write("Upload a payment screenshot and we'll extract your expense automatically.")

uploaded_file = st.file_uploader(
    "Upload Screenshot", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Your Screenshot", use_column_width=True)

    with st.spinner("Extracting text..."):
        raw_text = extract_text(image)
        parsed = parse_expense(raw_text)

    st.subheader("📋 Extracted Information")

    col1, col2, col3 = st.columns(3)
    col1.metric("Amount", f"₹{parsed['amount']}" if parsed['amount'] else "Not found")
    col2.metric("Date", parsed['date'] or "Not found")
    col3.metric("Merchant", parsed['merchant'] or "Not found")

    with st.expander("See raw OCR text"):
        st.text(raw_text)