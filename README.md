# EnterpriseIQ

A chat-based assistant for manufacturing teams that lets you query business data using plain language — no SQL or technical knowledge needed.

Built this as part of Gen AI Academy APAC 2026 (Track 2). The idea came from seeing how much time operations staff spend jumping between different systems just to answer simple questions like "how much aluminum do we have left?" or "what orders are still pending?"

## What it does

Connects to three data sources through a single chat interface:
- Production database — inventory, machine status, output metrics
- ERP system — orders, suppliers, customer records  
- Documents — maintenance logs, reports, SOPs in PDF or Excel

You ask in English or Bahasa Indonesia, it figures out where to look and gives you a straight answer.

## Stack

Python · Gemini 2.5 Flash · MCP · SQLite · Streamlit · Docker · Google Cloud Run

## Live

https://enterpriseiq-223602918704.asia-southeast1.run.app

## Run locally
```bash
git clone https://github.com/USERNAME/enterpriseiq
cd enterpriseiq
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python data/seed_db.py
streamlit run ui/app.py
```

Add your `GEMINI_API_KEY` to the `.env` file before running.
