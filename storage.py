# storage.py
# Stores expenses during the session using Streamlit session state

import streamlit as st
import pandas as pd
from datetime import datetime

def initialize_storage():
    """Creates empty expense list if it doesn't exist"""
    if 'expenses' not in st.session_state:
        st.session_state.expenses = []

def add_expense(amount, date, merchant, category, raw_text=""):
    """Adds one expense to the list"""
    initialize_storage()
    
    expense = {
        "amount": amount,
        "date": date or datetime.now().strftime("%d/%m/%Y"),
        "merchant": merchant or "Unknown",
        "category": category,
        "added_at": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    
    st.session_state.expenses.append(expense)

def get_all_expenses():
    """Returns all expenses as a pandas DataFrame"""
    initialize_storage()
    
    if not st.session_state.expenses:
        return pd.DataFrame()
    
    return pd.DataFrame(st.session_state.expenses)

def get_category_totals():
    """Returns total spending per category"""
    df = get_all_expenses()
    
    if df.empty:
        return {}
    
    # Group by category and sum amounts
    totals = df.groupby('category')['amount'].sum().to_dict()
    return totals

def get_total_spending():
    """Returns total amount spent"""
    df = get_all_expenses()
    if df.empty:
        return 0
    return df['amount'].sum()

def clear_expenses():
    """Clears all expenses"""
    st.session_state.expenses = []