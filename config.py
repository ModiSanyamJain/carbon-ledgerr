"""
CarbonLedger – Configuration Module
Loads database and application settings.
"""

import os

# ── SQLite Database Configuration ────────────────────────────────────────────
DB_PATH = os.path.join(os.path.dirname(__file__), "database", "carbonledger.db")

# ── Application Settings ─────────────────────────────────────────────────────
APP_TITLE = "CarbonLedger"
APP_SUBTITLE = "Industrial Carbon Footprint & Credit Exchange"
APP_VERSION = "1.0.0"

# ── Emission Factor Defaults (kg CO₂ per unit) ──────────────────────────────
DEFAULT_EMISSION_FACTORS = {
    "electricity_kwh": 0.85,        # kg CO2 per kWh
    "coal_tons": 2400.0,            # kg CO2 per ton  (2.4 t CO2/t coal)
    "gas_m3": 2.0,                  # kg CO2 per m³
    "transport_fuel_liters": 2.31,  # kg CO2 per litre
}

# ── Carbon Credit Conversion ─────────────────────────────────────────────────
CREDIT_CONVERSION_FACTOR = 1000.0  # 1 credit = 1 ton CO2 = 1000 kg CO2
