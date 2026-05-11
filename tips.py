# tips.py

# Tips based on famous financial gurus
# Adapted for Indian users

FINANCIAL_TIPS = {
    
    "🍔 Food & Dining": {
        "tip": "You're spending on food delivery. Cook at home more often — even 3 days a week can save ₹2000+ monthly.",
        "guru": "Warren Buffett",
        "guru_advice": "Buffett is famous for eating simple, cheap food despite being a billionaire. He says small daily savings compound into wealth.",
        "action": "Try cooking at home Monday to Wednesday. Use Swiggy/Zomato only on weekends.",
        "monthly_save_estimate": "₹1500 - ₹3000"
    },
    
    "🛒 Groceries": {
        "tip": "Groceries are a necessary expense. Focus on reducing waste — 30% of grocery spending is wasted food.",
        "guru": "Ramit Sethi",
        "guru_advice": "Sethi says 'spend consciously on things you love, cut mercilessly on things you don't'.",
        "action": "Make a weekly grocery list before shopping. Buy only what's on the list.",
        "monthly_save_estimate": "₹500 - ₹1000"
    },
    
    "🚗 Transport": {
        "tip": "Transport costs add up quickly. Consider metro or bus for regular commutes.",
        "guru": "Robert Kiyosaki",
        "guru_advice": "Kiyosaki says a car is a liability, not an asset. Minimize transport costs to invest the difference.",
        "action": "Use Namma Metro / BMTC for daily commute. Save cabs for emergencies.",
        "monthly_save_estimate": "₹1000 - ₹2500"
    },
    
    "🛍️ Shopping": {
        "tip": "Before buying anything, wait 48 hours. If you still want it, it's not impulse buying.",
        "guru": "Warren Buffett",
        "guru_advice": "Buffett's rule: 'If you don't need it, the price doesn't matter.'",
        "action": "Uninstall shopping apps from your phone. Only shop from desktop — it reduces impulse buying by 40%.",
        "monthly_save_estimate": "₹2000 - ₹5000"
    },
    
    "💡 Bills & Utilities": {
        "tip": "Bills are fixed expenses. Look for cheaper plans — Jio and Airtel have plans as low as ₹179/month.",
        "guru": "Ramit Sethi",
        "guru_advice": "Sethi recommends automating bill payments to avoid late fees and negotiating better rates annually.",
        "action": "Call your internet provider and ask for a better plan. Most companies have hidden cheaper options.",
        "monthly_save_estimate": "₹200 - ₹500"
    },
    
    "🎬 Entertainment": {
        "tip": "Are you using all your subscriptions? The average Indian pays for 3 streaming services but regularly uses only 1.",
        "guru": "Ramit Sethi",
        "guru_advice": "Sethi says to cut subscriptions you don't use — it's painless saving.",
        "action": "List all your subscriptions. Cancel any you haven't used in 2 weeks.",
        "monthly_save_estimate": "₹500 - ₹1500"
    },
    
    "🏥 Health": {
        "tip": "Health spending is an investment, not an expense. Don't cut here — but do compare pharmacy prices.",
        "guru": "General Principle",
        "guru_advice": "Netmeds and PharmEasy are typically 20-30% cheaper than local pharmacies for the same medicines.",
        "action": "Get a health insurance policy if you don't have one. Premiums are low when you're young.",
        "monthly_save_estimate": "₹200 - ₹800"
    },
    
    "📚 Education": {
        "tip": "Education spending is the best investment you can make. This is the one area to NOT cut.",
        "guru": "Warren Buffett",
        "guru_advice": "Buffett says 'the best investment you can make is in yourself. Nobody can take away what you have in your head.'",
        "action": "Look for free alternatives first — YouTube, free Coursera audits, NPTEL courses.",
        "monthly_save_estimate": "Invest more here!"
    },
    
    "🏦 Finance & Investment": {
        "tip": "Great — you're investing! Make sure you're following the 50/30/20 rule.",
        "guru": "Multiple Gurus",
        "guru_advice": "50% needs, 30% wants, 20% savings/investments. SIP in index funds is recommended by most experts for beginners.",
        "action": "Set up an automatic SIP on the 1st of every month so you invest before you can spend.",
        "monthly_save_estimate": "Compound this!"
    },
    
    "🏠 Rent & Housing": {
        "tip": "Rent should not exceed 30% of your monthly income. If it does, consider roommates or relocation.",
        "guru": "Robert Kiyosaki",
        "guru_advice": "Kiyosaki's famous advice: your house is not an asset if you're renting. Focus on investing the difference.",
        "action": "Calculate rent as % of income. If above 30%, look for a roommate to split costs.",
        "monthly_save_estimate": "₹3000 - ₹8000"
    },
    
    "📦 Other": {
        "tip": "Unrecognized expense. Track it manually to understand your spending better.",
        "guru": "General Advice",
        "guru_advice": "You can't manage what you don't measure. Track every rupee for one month.",
        "action": "Add this expense manually to your expense tracker with a proper category.",
        "monthly_save_estimate": "Varies"
    }
}


def get_tip(category):
    """Returns the tip for a given category"""
    return FINANCIAL_TIPS.get(category, FINANCIAL_TIPS["📦 Other"])