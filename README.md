# 💰 PocketSmart AI

PocketSmart AI is a Generative AI budgeting assistant. Users enter monthly income, expenses, and a financial goal. The application calculates the budget overview and uses Google Gemini to generate practical recommendations.

## Features

- Monthly income and expense inputs
- Expense breakdown chart
- Remaining-money calculation
- AI-generated budget recommendations
- Suggested needs/wants/savings plan
- Financial-goal guidance
- Streamlit web interface

## Tech Stack

- Python
- Streamlit
- Google Gemini API
- Google GenAI Python SDK
- python-dotenv

## Project Structure

```text
PocketSmart-AI/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/PocketSmart-AI.git
cd PocketSmart-AI
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Gemini

Copy `.env.example` to `.env` and set:

```text
GEMINI_API_KEY=your_gemini_api_key_here
```

Never commit `.env` or expose your API key.

### 5. Run

```bash
streamlit run app.py
```

## GitHub Upload

```bash
git init
git add .
git commit -m "Initial commit - PocketSmart AI"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/PocketSmart-AI.git
git push -u origin main
```

## Disclaimer

This is an educational Generative AI project. It provides general budgeting suggestions and is not professional financial advice.
