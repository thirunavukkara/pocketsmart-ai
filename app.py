import os
import json
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

st.set_page_config(
    page_title="PocketSmart AI",
    page_icon="💰",
    layout="wide"
)

API_KEY = os.getenv("GEMINI_API_KEY")

st.title("💰 PocketSmart AI")
st.caption("Your Smart Budget & Recommendation Assistant")

if not API_KEY:
    st.warning("Gemini API key not found. Add GEMINI_API_KEY to your .env file.")
    st.stop()

client = genai.Client(api_key=API_KEY)

st.sidebar.header("💵 Monthly Financial Details")

income = st.sidebar.number_input("Monthly Income (₹)", min_value=0.0, value=30000.0, step=1000.0)
rent = st.sidebar.number_input("Rent / Housing (₹)", min_value=0.0, value=8000.0, step=500.0)
food = st.sidebar.number_input("Food & Groceries (₹)", min_value=0.0, value=5000.0, step=500.0)
transport = st.sidebar.number_input("Transport (₹)", min_value=0.0, value=3000.0, step=500.0)
shopping = st.sidebar.number_input("Shopping (₹)", min_value=0.0, value=2000.0, step=500.0)
entertainment = st.sidebar.number_input("Entertainment (₹)", min_value=0.0, value=1500.0, step=500.0)
other = st.sidebar.number_input("Other Expenses (₹)", min_value=0.0, value=1000.0, step=500.0)
goal = st.sidebar.text_input("Financial Goal", "Build an emergency fund")

expenses = {
    "Rent / Housing": rent,
    "Food & Groceries": food,
    "Transport": transport,
    "Shopping": shopping,
    "Entertainment": entertainment,
    "Other": other,
}

total_expenses = sum(expenses.values())
remaining = income - total_expenses
savings_rate = (remaining / income * 100) if income else 0

st.markdown("### 📊 Monthly Overview")
c1, c2, c3 = st.columns(3)
c1.metric("Income", f"₹{income:,.0f}")
c2.metric("Expenses", f"₹{total_expenses:,.0f}")
c3.metric("Remaining", f"₹{remaining:,.0f}")

if remaining < 0:
    st.error("Your current expenses are higher than your income.")
elif remaining == 0:
    st.warning("Your income is fully allocated.")
else:
    st.success(f"You currently have ₹{remaining:,.0f} left after listed expenses.")

st.markdown("### 📋 Expense Breakdown")
st.bar_chart(expenses)

st.markdown("### 🤖 AI Budget Analysis")

if st.button("✨ Analyze My Budget", type="primary", use_container_width=True):
    expense_text = "\n".join(
        f"- {name}: ₹{amount:,.0f}" for name, amount in expenses.items()
    )

    prompt = f"""
You are PocketSmart AI, a budgeting assistant for an educational project.

Analyze this monthly budget:
Income: ₹{income:,.0f}
Expenses:
{expense_text}
Remaining: ₹{remaining:,.0f}
Financial goal: {goal}

Return ONLY valid JSON with these keys:
summary: string
savings_percentage: string
recommendations: array of 4 short strings
budget_plan: object with needs, wants, savings as string amounts
goal_advice: string

Keep advice practical and general. Do not provide regulated financial, investment,
loan, tax, or insurance advice. Do not claim certainty.
"""

    try:
        with st.spinner("Gemini is analyzing your budget..."):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={"response_mime_type": "application/json"},
            )

        data = json.loads(response.text)

        st.success("Analysis completed!")

        st.subheader("📝 Summary")
        st.write(data.get("summary", ""))

        st.subheader("💰 Suggested Savings")
        st.info(data.get("savings_percentage", "Not available"))

        st.subheader("🎯 Recommendations")
        for item in data.get("recommendations", []):
            st.write(f"✅ {item}")

        st.subheader("📊 Suggested Budget Plan")
        plan = data.get("budget_plan", {})
        p1, p2, p3 = st.columns(3)
        p1.metric("Needs", plan.get("needs", "—"))
        p2.metric("Wants", plan.get("wants", "—"))
        p3.metric("Savings", plan.get("savings", "—"))

        st.subheader("🎯 Goal Advice")
        st.write(data.get("goal_advice", ""))

    except json.JSONDecodeError:
        st.error("Gemini returned an unexpected response format. Please try again.")
    except Exception as exc:
        st.error("Could not complete the AI analysis.")
        st.exception(exc)

st.divider()
st.caption("PocketSmart AI • Generative AI Project • Gemini + Streamlit")
