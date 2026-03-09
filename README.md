# 🌿 CarbonLedger

**Industrial Carbon Footprint & Carbon Credit Exchange Platform**

CarbonLedger is a production-grade dashboard that enables industries to calculate carbon emissions, benchmark against peers, receive reduction recommendations, and trade carbon credits through a secure marketplace with full ACID transaction support.

---

## 📋 Prerequisites

| Tool     | Version   |
|----------|-----------|
| Python   | ≥ 3.10    |
| pip      | latest    |

> **No external database required.** CarbonLedger uses SQLite (built into Python) — the database is created automatically on first run with demo seed data.

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd carbonledger
pip install -r requirements.txt
```

### 2. Launch the Dashboard

```bash
streamlit run app.py
```

The app will open at **http://localhost:8501**.  
The SQLite database (`database/carbonledger.db`) is created and seeded automatically on the first launch.

---

## 🏗️ Project Structure

```
carbonledger/
├── app.py                        # Streamlit entry point
├── config.py                     # Settings & environment config
├── requirements.txt
├── README.md
│
├── database/
│   ├── schema.sql                # SQLite schema + seed data
│   └── init_db.py                # Auto-initialises the DB
│
├── backend/
│   ├── db_connection.py          # SQLite connection helper
│   ├── carbon_calculator.py      # Emission calculation engine
│   ├── industry_service.py       # Industry CRUD operations
│   ├── credit_marketplace.py     # Credit trading with ACID txns
│   ├── benchmarking_engine.py    # Sector benchmarking & ranking
│   └── recommendation_engine.py  # Emission reduction advisor
│
├── frontend/
│   ├── dashboard.py              # Main metrics & charts
│   ├── calculator_page.py        # Carbon emission calculator
│   ├── marketplace_page.py       # Credit exchange UI
│   ├── benchmarking_page.py      # Industry comparison view
│   └── history_page.py           # Emission history & trends
│
└── assets/
    └── styles.css                # Custom dark-theme CSS
```

---

## 🔑 Key Features

| Feature                     | Description                                              |
|-----------------------------|----------------------------------------------------------|
| 🏭 Facility Registration    | Register industrial facilities with sector & capacity    |
| 📊 Emission Calculator      | Compute CO₂ from electricity, coal, gas, transport       |
| 📈 Emission History         | Track & visualize emission trends over time              |
| 🏅 Industry Benchmarking    | Compare against sector averages & get percentile rank    |
| 💡 Reduction Recommendations| Rule-based advisor for lowering emissions                |
| 💱 Credit Marketplace       | List, buy, & sell carbon credits                         |
| 🔒 ACID Transactions        | Secure credit trades with SQLite BEGIN/COMMIT/ROLLBACK   |

---

## 🧪 ACID Transaction Example

The marketplace module wraps every credit trade in a transaction:

```python
BEGIN IMMEDIATE
  → Deduct credits from seller's balance
  → Add credits to buyer's balance
  → Update listing status
  → Insert transaction record
COMMIT
```

If any step fails, the entire transaction is **rolled back** automatically.

---

## 📄 License

MIT License – free for educational and industrial use.
