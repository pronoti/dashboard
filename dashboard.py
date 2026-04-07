import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import dcc, html
from pathlib import Path

COUNTRY_CODE = "TUR"
COUNTRY_NAME = "Türkiye"
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# ── Data loading ───────────────────────────────────────────────────────────────

def load_gdp():
    df = pd.read_csv(DATA_DIR / "GDP GROWTH.csv", low_memory=False)
    df = df[df["REF_AREA"] == COUNTRY_CODE][["TIME_PERIOD", "OBS_VALUE"]].dropna()
    return df.astype({"TIME_PERIOD": int, "OBS_VALUE": float}).sort_values("TIME_PERIOD")

def load_world_gdp():
    df = pd.read_csv(DATA_DIR / "GDP GROWTH.csv", low_memory=False)
    df = df[df["REF_AREA"] == "WLD"][["TIME_PERIOD", "OBS_VALUE"]].dropna()
    return df.astype({"TIME_PERIOD": int, "OBS_VALUE": float}).sort_values("TIME_PERIOD")

def load_trade(filename):
    df = pd.read_csv(DATA_DIR / filename, low_memory=False)
    df = df[(df["REF_AREA"] == COUNTRY_CODE) & (df["UNIT_MEASURE"] == "PT_GDP")]
    return (df[["TIME_PERIOD", "OBS_VALUE"]].dropna()
              .astype({"TIME_PERIOD": int, "OBS_VALUE": float})
              .sort_values("TIME_PERIOD"))

def load_unemployment():
    df = pd.read_csv(DATA_DIR / "unemployment.csv", low_memory=False)
    df = df[
        (df["REF_AREA_ID"] == COUNTRY_CODE) &
        (df["COMP_BREAKDOWN_1_ID"] == "GS_TCZ") &
        (df["AGE_ID"] == "Y15T24") &
        (df["OBS_STATUS_ID"] == "A")
    ]
    result = {}
    for sex, label in [("M", "Male"), ("F", "Female")]:
        sub = (df[df["SEX_ID"] == sex][["TIME_PERIOD", "OBS_VALUE"]]
                 .dropna()
                 .astype({"TIME_PERIOD": int, "OBS_VALUE": float})
                 .sort_values("TIME_PERIOD"))
        result[label] = sub
    result["Total"] = pd.DataFrame(columns=["TIME_PERIOD", "OBS_VALUE"])
    return result

def load_world_trade(filename):
    df = pd.read_csv(DATA_DIR / filename, low_memory=False)
    df = df[df["UNIT_MEASURE"] == "PT_GDP"][["REF_AREA", "TIME_PERIOD", "OBS_VALUE"]].dropna()
    df = df.astype({"TIME_PERIOD": int, "OBS_VALUE": float})
    return df.groupby("TIME_PERIOD", as_index=False)["OBS_VALUE"].mean().sort_values("TIME_PERIOD")

def load_world_unemployment():
    df = pd.read_csv(DATA_DIR / "unemployment.csv", low_memory=False)
    df = df[
        (df["REF_AREA_ID"] == "WLD") &
        (df["COMP_BREAKDOWN_1_ID"] == "GS_TCZ") &
        (df["AGE_ID"] == "Y15T24") &
        (df["OBS_STATUS_ID"] == "A")
    ]
    result = {}
    for sex, label in [("M", "Male"), ("F", "Female")]:
        sub = (df[df["SEX_ID"] == sex][["TIME_PERIOD", "OBS_VALUE"]]
                 .dropna()
                 .astype({"TIME_PERIOD": int, "OBS_VALUE": float})
                 .sort_values("TIME_PERIOD"))
        result[label] = sub
    return result

def load_inflation():
    df = pd.read_csv(DATA_DIR / "Inflation.csv", low_memory=False)
    df = df[(df["REF_AREA"] == COUNTRY_CODE) & (df["OBS_STATUS"] == "A")]
    df = (df[["TIME_PERIOD", "OBS_VALUE"]].dropna()
            .astype({"TIME_PERIOD": int, "OBS_VALUE": float})
            .sort_values("TIME_PERIOD"))
    df["inflation_rate"] = df["OBS_VALUE"].pct_change() * 100
    return df.dropna()

# Load all data
gdp = load_gdp()
world_gdp = load_world_gdp()
exp = load_trade("Exports.csv")
imp = load_trade("imports.csv")
world_exp = load_world_trade("Exports.csv")
world_imp = load_world_trade("imports.csv")
unem = load_unemployment()
world_unem = load_world_unemployment()
infl = load_inflation()

# Trade balance
trade = pd.merge(exp, imp, on="TIME_PERIOD", suffixes=("_exp", "_imp"))
trade["balance"] = trade["OBS_VALUE_exp"] - trade["OBS_VALUE_imp"]

# ── Figures ────────────────────────────────────────────────────────────────────

# 1. GDP Growth
fig_gdp = px.line(gdp, x="TIME_PERIOD", y="OBS_VALUE",
                  labels={"TIME_PERIOD": "Year", "OBS_VALUE": "GDP Growth (%)"},
                  title="GDP Growth Rate (Annual %)")
fig_gdp.add_hline(y=0, line_dash="dash", line_color="red", opacity=0.5)
fig_gdp.update_traces(line_color="#1f77b4", line_width=2.5, mode="lines+markers",
                      marker=dict(size=5))
fig_gdp.add_trace(go.Scatter(
    x=world_gdp["TIME_PERIOD"], y=world_gdp["OBS_VALUE"],
    mode="lines", name="World Avg",
    line=dict(color="#ff7f0e", width=1.5, dash="dot"),
))
fig_gdp.update_layout(template="plotly_white", hovermode="x unified")

# 2. Trade
fig_trade = go.Figure([
    go.Bar(x=exp["TIME_PERIOD"], y=exp["OBS_VALUE"], name="Exports (% GDP)",
           marker_color="#2ca02c"),
    go.Bar(x=imp["TIME_PERIOD"], y=imp["OBS_VALUE"], name="Imports (% GDP)",
           marker_color="#d62728"),
])
fig_trade.update_layout(barmode="group", template="plotly_white",
                        title="Exports & Imports (% of GDP)",
                        xaxis_title="Year", yaxis_title="% of GDP",
                        hovermode="x unified")
fig_trade.add_trace(go.Scatter(
    x=world_exp["TIME_PERIOD"], y=world_exp["OBS_VALUE"],
    mode="lines", name="Cross-country Avg Exports",
    line=dict(color="#2ca02c", width=1.5, dash="dot")
))
fig_trade.add_trace(go.Scatter(
    x=world_imp["TIME_PERIOD"], y=world_imp["OBS_VALUE"],
    mode="lines", name="Cross-country Avg Imports",
    line=dict(color="#d62728", width=1.5, dash="dot")
))

# 3. Trade Balance
fig_balance = go.Figure()
fig_balance.add_trace(go.Scatter(
    x=trade["TIME_PERIOD"], y=trade["balance"],
    fill="tozeroy",
    fillcolor="rgba(214,39,40,0.2)",
    line=dict(color="#d62728", width=2),
    name="Trade Balance"
))
fig_balance.add_hline(y=0, line_dash="dash", line_color="black", opacity=0.4)
fig_balance.update_layout(template="plotly_white",
                          title="Trade Balance (Exports − Imports, % of GDP)",
                          xaxis_title="Year", yaxis_title="% of GDP")

# 4. Unemployment
fig_unem = go.Figure()
colors = {"Total": "#7f7f7f", "Male": "#1f77b4", "Female": "#e377c2"}
for label, df_u in unem.items():
    if not df_u.empty:
        fig_unem.add_trace(go.Scatter(
            x=df_u["TIME_PERIOD"], y=df_u["OBS_VALUE"],
            mode="lines+markers", name=label,
            line=dict(color=colors[label], width=2),
            marker=dict(size=5)
        ))
for label, color in [("Male", "#aec7e8"), ("Female", "#f7b6d2")]:
    df_wu = world_unem.get(label, pd.DataFrame())
    if not df_wu.empty:
        fig_unem.add_trace(go.Scatter(
            x=df_wu["TIME_PERIOD"], y=df_wu["OBS_VALUE"],
            mode="lines", name=f"World {label}",
            line=dict(color=color, width=1.5, dash="dot"),
        ))
fig_unem.update_layout(template="plotly_white",
                       title="Unemployment Rate by Gender (%, Ages 15–24)",
                       xaxis_title="Year", yaxis_title="Unemployment (%)",
                       hovermode="x unified")

# 5. Inflation
fig_infl = px.line(infl, x="TIME_PERIOD", y="inflation_rate",
                   title="Inflation Rate — Average Consumer Prices (Annual %)",
                   labels={"TIME_PERIOD": "Year", "inflation_rate": "Inflation (%)"})
fig_infl.add_hline(y=0, line_dash="dash", line_color="black", opacity=0.3)
fig_infl.update_traces(line_color="#ff7f0e", line_width=2.5,
                       mode="lines+markers", marker=dict(size=4))
fig_infl.update_layout(template="plotly_white", hovermode="x unified")

# 6. Overview horizontal bar
_indicators = ["Inflation", "Youth Unemp (M)", "Youth Unemp (F)", "Trade Balance", "Imports", "Exports", "GDP Growth"]
_values = [
    round(float(infl["inflation_rate"].iloc[-1]), 2) if not infl.empty else 0,
    round(float(unem["Male"]["OBS_VALUE"].iloc[-1]), 2) if not unem["Male"].empty else 0,
    round(float(unem["Female"]["OBS_VALUE"].iloc[-1]), 2) if not unem["Female"].empty else 0,
    round(exp["OBS_VALUE"].iloc[-1] - imp["OBS_VALUE"].iloc[-1], 2),
    round(float(imp["OBS_VALUE"].iloc[-1]), 2),
    round(float(exp["OBS_VALUE"].iloc[-1]), 2),
    round(float(gdp["OBS_VALUE"].iloc[-1]), 2),
]
_colors = [
    "#d62728", "#1f77b4", "#e377c2",
    "#2ca02c" if _values[3] >= 0 else "#d62728",
    "#d62728", "#2ca02c",
    "#2ca02c" if _values[6] >= 0 else "#d62728",
]

fig_overlay = go.Figure(go.Bar(
    x=_values, y=_indicators,
    orientation="h",
    marker_color=_colors,
    text=[f"{v}%" for v in _values],
    textposition="auto",
))
fig_overlay.update_layout(
    title="Türkiye Economic Indicators Overview (Latest Values)",
    template="plotly_white",
    xaxis=dict(
        title="Value (%)",
        range=[min(min(_values) - 10, -10), max(_values) + 30]
    ),
    yaxis=dict(autorange="reversed"),
    height=420,
    margin=dict(l=180, r=100, t=50, b=40),
)


# ── KPI Helper Functions ───────────────────────────────────────────────────────

def last_value(df, col="OBS_VALUE"):
    return round(float(df[col].iloc[-1]), 2) if not df.empty else "N/A"

def kpi_card(title, value, unit="", color="#1f77b4"):
    return html.Div([
        html.H4(title, style={"margin": "0 0 8px", "fontSize": "14px", "color": "#666"}),
        html.H2(f"{value}{unit}", style={"margin": "0", "color": color, "fontSize": "28px"})
    ], style={
        "background": "white", "padding": "20px", "borderRadius": "8px",
        "textAlign": "center", "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
        "border": "1px solid #e0e0e0"
    })

# Calculate KPI values
gdp_latest = last_value(gdp)
exp_latest = last_value(exp)
imp_latest = last_value(imp)
infl_latest = round(float(infl["inflation_rate"].iloc[-1]), 2) if not infl.empty else "N/A"
unem_male = unem.get("Male", pd.DataFrame())
unem_latest = last_value(unem_male) if not unem_male.empty else "N/A"
trade_balance = round(exp_latest - imp_latest, 2) if isinstance(exp_latest, float) and isinstance(imp_latest, float) else "N/A"
gdp_latest_year = int(gdp["TIME_PERIOD"].iloc[-1]) if not gdp.empty else "N/A"
trade_latest_year = int(exp["TIME_PERIOD"].iloc[-1]) if not exp.empty else "N/A"
unem_latest_year = int(unem_male["TIME_PERIOD"].iloc[-1]) if not unem_male.empty else "N/A"
infl_latest_year = int(infl["TIME_PERIOD"].iloc[-1]) if not infl.empty else "N/A"

# ── Dash App ───────────────────────────────────────────────────────────────────

app = dash.Dash(__name__)
app.title = f"{COUNTRY_NAME} Economic Dashboard"

app.layout = html.Div([
    # Header
    html.Div([
        html.H1(f"{COUNTRY_NAME} Economic Dashboard",
                style={"textAlign": "center", "color": "white", "margin": "0"}),
        html.P("Macroeconomic indicators for Türkiye", 
               style={"textAlign": "center", "color": "#ccc", "margin": "10px 0 0"})
    ], style={
        "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "padding": "30px", "marginBottom": "20px"
    }),
    
    # KPI Cards Row
    html.Div([
        html.H3("Key Performance Indicators", style={"marginBottom": "15px", "color": "#333"}),
        html.Div([
            kpi_card("GDP Growth", gdp_latest, "%", "#2ca02c" if isinstance(gdp_latest, float) and gdp_latest >= 0 else "#d62728"),
            kpi_card("Exports", exp_latest, "% GDP", "#2ca02c"),
            kpi_card("Imports", imp_latest, "% GDP", "#d62728"),
            kpi_card("Trade Balance", trade_balance, "% GDP", "#2ca02c" if isinstance(trade_balance, float) and trade_balance >= 0 else "#d62728"),
            kpi_card("Youth Unemployment", unem_latest, "%", "#ff7f0e"),
            kpi_card("Inflation Rate", infl_latest, "%", "#d62728" if isinstance(infl_latest, float) and infl_latest > 5 else "#ff7f0e")
        ], style={
            "display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(200px, 1fr))",
            "gap": "15px", "marginBottom": "30px"
        })
    ], style={"padding": "0 20px"}),

    # Charts Section
    html.Div([
        html.H3("Economic Indicators Analysis", style={"marginBottom": "20px", "color": "#333"}),
        
        # Row 1: GDP and Trade
        html.Div([
            html.Div([dcc.Graph(figure=fig_gdp)], style={"width": "50%"}),
            html.Div([dcc.Graph(figure=fig_trade)], style={"width": "50%"})
        ], style={"display": "flex", "marginBottom": "20px"}),
        
        # Row 2: Trade Balance and Unemployment
        html.Div([
            html.Div([dcc.Graph(figure=fig_balance)], style={"width": "50%"}),
            html.Div([dcc.Graph(figure=fig_unem)], style={"width": "50%"})
        ], style={"display": "flex", "marginBottom": "20px"}),
        
        # Row 3: Inflation and Overview
        html.Div([
            html.Div([dcc.Graph(figure=fig_infl)], style={"width": "50%"}),
            html.Div([dcc.Graph(figure=fig_overlay)], style={"width": "50%"})
        ], style={"display": "flex", "marginBottom": "20px"})
        
    ], style={"padding": "0 20px"}),
    
    # Footer
    html.Div([
        html.P(
            "Data sources: World Bank WDI, World Bank Gender Statistics, and IMF WEO.",
               style={"textAlign": "center", "color": "#666", "margin": "0"})
    ], style={"padding": "20px", "borderTop": "1px solid #eee", "marginTop": "30px"})
    
], style={"fontFamily": "Arial, sans-serif", "backgroundColor": "#f5f5f5", "minHeight": "100vh"})

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=8050)
