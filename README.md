# 🔍 QueryLens

**Inspect, query, and visualize your Appwrite databases using plain English.**

QueryLens is an AI-powered database GUI designed for the **Appwrite TablesDB Hackathon**. It translates natural language questions into structured queries against Appwrite databases, executing queries locally via open-source LLMs (Phi-3 / Ollama) and visualizing results through an intuitive, interactive Streamlit interface.

---

## ✨ Features

* **🗣️ Plain English Querying:** Ask questions in natural language (e.g., *"Show all active users with budget over 500"*).
* **🤖 Local LLM Engine:** Powered by local models (`Ollama` + `Phi-3`) for fast, private, and offline-capable query generation.
* **⚡ Appwrite TablesDB Integration:** Connects directly to Appwrite databases and collections using the latest `appwrite` SDK.
* **🛡️ Built-in Resiliency:** Includes automatic fallback mechanisms to ensure uninterrupted UI development and testing.
* **📊 Interactive Visualizations:** Auto-generates tabular data grids, key summary metrics, and dynamic bar charts based on retrieved records.

---

## 🛠️ Project Architecture

```text
QueryLens/
├── app.py                  # Main Streamlit dashboard application
├── core/
│   ├── appwrite_client.py  # Appwrite TablesDB authentication & data fetching
│   ├── query_engine.py     # Natural language translation via local Ollama LLM
│   └── visualizer.py       # Data tables, key metrics, and auto-charting components
├── .env                    # Environment credentials (API keys, endpoints, IDs)
└── requirements.txt        # Python dependencies
