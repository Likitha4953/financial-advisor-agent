# app.py — Full Week 2 Version (Windows Fixed)

import streamlit as st
from PIL import Image
import pytesseract
import cv2
import numpy as np
import re
import matplotlib.pyplot as plt

# ---- WINDOWS TESSERACT FIX ----
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Import our other files
from categorizer import categorize_expense, get_spending_level
from tips import get_tip
from storage import (initialize_storage, add_expense,
                     get_all_expenses, get_category_totals,
                     get_total_spending, clear_expenses)


# ---- IMAGE PROCESSING ----

def preprocess_image(pil_image):
    img = np.array(pil_image)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    
    # Make image much bigger for better OCR
    scale = 3  # increased from 2 to 3
    width = int(gray.shape[1] * scale)
    height = int(gray.shape[0] * scale)
    enlarged = cv2.resize(gray, (width, height),
                          interpolation=cv2.INTER_CUBIC)
    
    # Strong denoising
    denoised = cv2.fastNlMeansDenoising(enlarged, h=30)
    
    # Sharpen
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened = cv2.filter2D(denoised, -1, kernel)
    
    # Threshold
    _, thresh = cv2.threshold(sharpened, 0, 255,
                               cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return Image.fromarray(thresh)


def extract_text(pil_image):
    processed = preprocess_image(pil_image)
    
    # Try 4 different OCR modes
    configs = [
        '--psm 6',   # uniform block of text
        '--psm 4',   # single column
        '--psm 11',  # sparse text
        '--psm 3',   # fully automatic
    ]
    
    results = []
    for config in configs:
        text = pytesseract.image_to_string(processed, config=config)
        results.append(text)
    
    # Return longest result (most text extracted)
    return max(results, key=len)


# ---- EXPENSE PARSER ----

def parse_expense(text):
    result = {"amount": None, "date": None, "merchant": None}

    # ---- AMOUNT: Use the exact pattern that worked ----
    # First try: "Total" followed by amount
    total_match = re.search(r'Total[^0-9]*(\d+\.\d{2})', text, re.IGNORECASE)
    if total_match:
        result["amount"] = float(total_match.group(1))
    
    # Second try: find all decimals, pick biggest
    if not result["amount"]:
        all_decimals = re.findall(r'\b(\d{2,6}\.\d{2})\b', text)
        if all_decimals:
            values = [float(x) for x in all_decimals]
            result["amount"] = max(values)

    # ---- DATE ----
    date_match = re.search(r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}', text)
    if date_match:
        result["date"] = date_match.group(0)

    # ---- MERCHANT ----
    known = {
        'swiggy': 'Swiggy', 'zomato': 'Zomato',
        'amazon': 'Amazon', 'flipkart': 'Flipkart',
        'uber': 'Uber', 'ola': 'Ola',
        'netflix': 'Netflix', 'bigbasket': 'BigBasket',
        'phonepe': 'PhonePe', 'gpay': 'Google Pay',
        'paytm': 'Paytm', 'jio': 'Jio', 'airtel': 'Airtel',
        'blinkit': 'Blinkit', 'zepto': 'Zepto',
    }
    for k, v in known.items():
        if k in text.lower():
            result["merchant"] = v
            break

    return result

# ---- SPENDING CHART ----

def show_spending_chart(category_totals):
    if not category_totals:
        return

    fig, ax = plt.subplots(figsize=(6, 4))

    categories = list(category_totals.keys())
    amounts = list(category_totals.values())
    colors = [
        '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4',
        '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F'
    ]

    ax.pie(
        amounts,
        labels=categories,
        colors=colors[:len(categories)],
        autopct='%1.1f%%',
        startangle=90
    )
    ax.set_title('Spending by Category')
    st.pyplot(fig)


# ---- MAIN APP ----

st.set_page_config(
    page_title="💰 Financial Advisor",
    page_icon="💰",
    layout="wide"
)

initialize_storage()

st.title("💰 Financial Advisor & Expense Manager")
st.markdown("Upload your payment screenshots and track your spending automatically.")

# Two column layout
col_left, col_right = st.columns([1, 1])

# ---- LEFT COLUMN: Upload & Analyze ----
with col_left:
    st.subheader("📸 Upload Payment Screenshot")

    uploaded_file = st.file_uploader(
        "Supports PhonePe, GPay, Paytm, Bank screenshots",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Screenshot",
                 use_column_width=True)

        with st.spinner("Analyzing your expense..."):
            raw_text = extract_text(image)
            parsed = parse_expense(raw_text)
            category = categorize_expense(
                parsed["merchant"], parsed["amount"], raw_text)
            level = get_spending_level(parsed["amount"], category)
            tip_data = get_tip(category)

        # Extracted Info
        st.subheader("📋 Extracted Information")
        c1, c2, c3 = st.columns(3)
        c1.metric(
            "Amount",
            f"₹{parsed['amount']}" if parsed['amount'] else "Not found"
        )
        c2.metric(
            "Merchant",
            parsed['merchant'] or "Not found"
        )
        c3.metric(
            "Date",
            parsed['date'] or "Not found"
        )

        # Category
        st.subheader("🏷️ Category Detected")
        st.markdown(f"### {category}")
        st.markdown(f"Spending Level: **{level}**")

        # Financial Tip
        st.subheader("💡 Financial Tip")
        st.info(f"**{tip_data['tip']}**")

        with st.expander(f"📖 What does {tip_data['guru']} say?"):
            st.write(tip_data['guru_advice'])
            st.markdown(f"**✅ Action:** {tip_data['action']}")
            st.markdown(f"**💰 Potential Monthly Saving:** {tip_data['monthly_save_estimate']}")

        # Save Button
        st.subheader("💾 Save This Expense")
        if parsed['amount']:
            if st.button("✅ Save Expense"):
                add_expense(
                    parsed['amount'],
                    parsed['date'],
                    parsed['merchant'],
                    category,
                    raw_text
                )
                st.success("Expense saved successfully!")
        else:
            st.warning("Amount not detected. Please enter manually:")
            manual_amount = st.number_input(
                "Enter Amount (₹)", min_value=0.0, step=1.0)
            manual_merchant = st.text_input("Enter Merchant Name")
            if st.button("✅ Save Manual Expense"):
                add_expense(
                    manual_amount,
                    parsed['date'],
                    manual_merchant or parsed['merchant'],
                    category,
                    raw_text
                )
                st.success("Expense saved!")

        # Debug Section
        with st.expander("🔍 Raw OCR Text (Debug)"):
            st.text(raw_text)

    else:
        st.info("👆 Upload a screenshot to get started")


# ---- RIGHT COLUMN: Dashboard ----
with col_right:
    st.subheader("📊 Spending Dashboard")

    df = get_all_expenses()
    total = get_total_spending()
    category_totals = get_category_totals()

    if df.empty:
        st.info("No expenses saved yet. Upload a screenshot and click Save!")

    else:
        # Top metrics
        m1, m2 = st.columns(2)
        m1.metric("💸 Total Spent", f"₹{total:,.2f}")
        m2.metric("🧾 Transactions", len(df))

        # Pie chart
        st.subheader("🥧 Spending Breakdown")
        show_spending_chart(category_totals)

        # Category totals
        st.subheader("📂 Category Wise Total")
        for cat, amt in category_totals.items():
            st.write(f"{cat} → ₹{amt:,.2f}")

        # Full expense table
        st.subheader("📝 All Expenses")
        st.dataframe(
            df[['date', 'merchant', 'amount', 'category']],
            use_column_width=True
        )

        # Clear all
        if st.button("🗑️ Clear All Expenses"):
            clear_expenses()
            st.rerun()
