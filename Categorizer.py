# categorizer.py

def categorize_expense(merchant, amount, raw_text):
    """
    Takes merchant name + raw OCR text
    Returns category and subcategory
    """
    
    text_lower = raw_text.lower()
    merchant_lower = merchant.lower() if merchant else ""
    
    # ---- CATEGORY RULES ----
    # Each category has keywords to look for
    
    categories = {
        
        "🍔 Food & Dining": [
            'swiggy', 'zomato', 'dominos', 'pizza', 'kfc', 'mcdonalds',
            'burger', 'restaurant', 'cafe', 'hotel', 'food', 'biryani',
            'dunzo', 'blinkit', 'zepto', 'instamart', 'dining', 'eat'
        ],
        
        "🛒 Groceries": [
            'bigbasket', 'grofers', 'dmart', 'reliance fresh', 'more',
            'supermarket', 'grocery', 'vegetables', 'fruits', 'milk',
            'bread', 'provisions', 'departmental'
        ],
        
        "🚗 Transport": [
            'uber', 'ola', 'rapido', 'auto', 'cab', 'taxi', 'metro',
            'bus', 'train', 'irctc', 'petrol', 'fuel', 'parking',
            'toll', 'namma metro', 'bmtc'
        ],
        
        "🛍️ Shopping": [
            'amazon', 'flipkart', 'myntra', 'ajio', 'nykaa', 'meesho',
            'snapdeal', 'shopping', 'clothes', 'shoes', 'fashion'
        ],
        
        "💡 Bills & Utilities": [
            'electricity', 'bescom', 'mseb', 'water', 'gas', 'lpg',
            'broadband', 'wifi', 'internet', 'postpaid', 'prepaid',
            'recharge', 'jio', 'airtel', 'vi ', 'bsnl'
        ],
        
        "🎬 Entertainment": [
            'netflix', 'hotstar', 'prime', 'spotify', 'youtube',
            'bookmyshow', 'movie', 'cinema', 'pvr', 'inox', 'gaming',
            'steam', 'playstation'
        ],
        
        "🏥 Health": [
            'pharmacy', 'medical', 'hospital', 'doctor', 'clinic',
            'apollo', 'medplus', 'netmeds', 'pharmeasy', 'healthkart',
            'gym', 'fitness', '1mg'
        ],
        
        "📚 Education": [
            'udemy', 'coursera', 'unacademy', 'byju', 'vedantu',
            'book', 'stationery', 'college', 'school', 'tuition',
            'course', 'class'
        ],
        
        "🏦 Finance & Investment": [
            'zerodha', 'groww', 'upstox', 'etmoney', 'mutual fund',
            'sip', 'insurance', 'lic', 'loan', 'emi', 'credit card'
        ],
        
        "🏠 Rent & Housing": [
            'rent', 'maintenance', 'society', 'housing', 'pg',
            'hostel', 'accommodation', 'nobroker'
        ],
    }
    
    # Check merchant name first, then full OCR text
    combined = merchant_lower + " " + text_lower
    
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in combined:
                return category
    
    # If nothing matched
    return "📦 Other"


def get_spending_level(amount, category):
    """
    Tells if spending is Low / Medium / High
    based on typical Indian spending patterns
    """
    
    # Average monthly budgets per category (in INR)
    typical_per_transaction = {
        "🍔 Food & Dining": {"low": 100, "high": 500},
        "🛒 Groceries": {"low": 200, "high": 1000},
        "🚗 Transport": {"low": 50, "high": 300},
        "🛍️ Shopping": {"low": 500, "high": 2000},
        "💡 Bills & Utilities": {"low": 200, "high": 1000},
        "🎬 Entertainment": {"low": 100, "high": 500},
        "🏥 Health": {"low": 100, "high": 500},
        "📚 Education": {"low": 500, "high": 2000},
    }
    
    if category in typical_per_transaction and amount:
        limits = typical_per_transaction[category]
        if amount <= limits["low"]:
            return "🟢 Low"
        elif amount <= limits["high"]:
            return "🟡 Medium"
        else:
            return "🔴 High"
    
    return "⚪ Unknown"