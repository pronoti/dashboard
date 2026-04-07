# Turkey Economic Dashboard

A Dash app that visualizes selected macroeconomic indicators for Turkey using local CSV datasets.

## Included indicators
- GDP growth
- Exports and imports (as % of GDP)
- Trade balance (exports minus imports)
- Youth unemployment (male/female, ages 15-24)
- Inflation proxy derived from CPI index year-over-year change

## Project structure
- `dashboard.py`: main Dash app and chart logic
- `data/`: source CSV files
- `report/`: supplementary report document

## Setup
1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run
```bash
python dashboard.py
```

Then open `http://127.0.0.1:8050`.

## Data freshness note
The datasets have different latest years, so KPI cards display each metric's own latest year.
