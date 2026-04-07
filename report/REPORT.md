# Economic Report Dashboard: Turkey

## Table of Contents

1. [List of Figures](#list-of-figures)
2. [List of Tables](#list-of-tables)
3. [Introduction](#introduction)
   1. [Country Overview](#country-overview)
4. [Data Set](#data-set)
   1. [Data Sources](#data-sources)
   2. [GDP Growth](#gdp-growth)
   3. [Exports and Imports](#exports-and-imports)
   4. [Trade Balance](#trade-balance)
   5. [Youth Unemployment](#youth-unemployment)
   6. [Inflation Rate](#inflation-rate)
   7. [Interesting Attributes](#interesting-attributes)
5. [Visualisations and Analysis](#visualisations-and-analysis)
   1. [Design Rationale](#design-rationale)
   2. [Overview](#overview)
   3. [GDP Growth Rate](#gdp-growth-rate)
   4. [Exports and Imports](#exports-and-imports-1)
   5. [Trade Balance](#trade-balance-1)
   6. [Youth Unemployment by Gender](#youth-unemployment-by-gender)
   7. [Inflation Rate](#inflation-rate-1)
   8. [Turkey Economic Indicators Overview](#turkey-economic-indicators-overview)
6. [Limitations and Validity](#limitations-and-validity)
7. [Conclusion](#conclusion)
8. [References](#references)

---

## List of Figures

1. Figure 1. Overview page of the dashboard.
2. Figure 2. GDP growth.
3. Figure 3. Exports and imports.
4. Figure 4. Trade balance.
5. Figure 5. Youth unemployment by gender.
6. Figure 6. Inflation rate.
7. Figure 7. Turkey economic indicators overview.

## List of Tables

No standalone analytical tables are required for this report.

---

## Introduction

Turkey is one of the largest emerging economies in the world, bridging Europe and Asia with a population exceeding 85 million. In this assignment, the dashboard is used to explore macroeconomic indicators that characterise Turkey's economic performance over recent decades. The visualisations are designed to provide a coherent picture of Turkey's economic trajectory, highlighting both growth potential and structural vulnerabilities.

### Country Overview

This project presents an interactive data visualisation dashboard analysing key economic indicators for Turkey, including GDP growth, exports and imports as a percentage of GDP, trade balance, youth unemployment by gender, and inflation rate. These indicators were selected because they jointly reflect macroeconomic momentum, external-sector performance, labour market pressure, and price stability. By comparing Turkey's data with world averages where relevant, the dashboard adds context that supports stronger interpretation and avoids country-only reading of trends.

---

## Data Set

This section examines the dataset breadth, key attributes, and preparation logic used to build the dashboard.

### Data Sources

The data sources used for this assignment are as follows.

- GDP growth (annual %): World Bank WDI series for country and world aggregates [1].
- Exports of goods and services (% of GDP): World Bank WDI series [2].
- Imports of goods and services (% of GDP): World Bank WDI series [3].
- Youth unemployment rate by gender (ages 15-24): ILO/World Bank stream [4].
- Inflation proxy from CPI index: IMF WEO index series via Data360 [5].

Data links are listed in full in the References section.

### GDP Growth

This dataset provides annual GDP growth rates as percentage change from the previous year across countries and aggregates. For this dashboard, the data was filtered to Turkey (`TUR`) and the world aggregate (`WLD`) to enable direct contextual comparison. The series is long enough to support multi-decade trend interpretation and the identification of expansion, contraction, and recovery phases.

### Exports and Imports

These datasets provide exports and imports of goods and services as a percentage of GDP. Expressing trade flows relative to GDP makes comparison across years more meaningful than nominal values alone. Rows were filtered to `UNIT_MEASURE = PT_GDP` to preserve consistency across the plotted time series.

### Trade Balance

Trade balance is a derived measure computed as exports minus imports (both as % of GDP). A positive value indicates surplus and a negative value indicates deficit. The metric was calculated by joining export and import series on year and then taking the difference.

### Youth Unemployment

This dataset provides annual youth unemployment (ages 15-24), disaggregated by sex. The pipeline filters to Turkey, total economy classification, and confirmed observations so the resulting series is comparable across years and suitable for gender-based labour market analysis.

### Inflation Rate

The inflation dataset is modelled from a CPI index series by computing year-on-year percentage change. Rows with confirmed observation status are retained before modelling. This produces a consistent inflation proxy that captures long-run price dynamics and recent high-inflation episodes.

### Interesting Attributes

Turkey's macroeconomic profile shows several features that justify focused analysis. GDP growth is dynamic but volatile; trade flows show persistent deficit pressure; youth unemployment is elevated with a sustained gender gap; and inflation has reached extreme levels in recent years. The dashboard also makes clear that source series end in different years, so latest-value comparisons must be interpreted as a recent snapshot rather than a strict same-year panel.

---

## Visualisations and Analysis

This section presents the key dashboard visuals and the intended analytical interpretation for each.

### Design Rationale

Chart types were selected to match both data structure and analytical objective. Line charts are used where trend continuity and turning points are critical, grouped bars are used where within-year two-variable comparison is needed, and an area chart around zero is used to make deficit magnitude immediately visible. KPI cards provide rapid orientation, while the horizontal overview chart supports compact cross-indicator comparison. Color is used semantically so concerning indicators read quickly without obscuring exact values.

### Overview

The overview page provides KPI cards so a user can immediately understand the current state of key indicators without being overloaded by detail. The cards display latest values for GDP growth, exports, imports, trade balance, youth unemployment, and inflation. This creates an immediate summary that signals a mixed macroeconomic profile: positive growth potential alongside persistent trade deficit, elevated youth unemployment, and high inflation. To improve analytical validity, each KPI includes its own latest year because the underlying source series do not terminate in the same period.

### GDP Growth Rate

The GDP growth chart plots Turkey's annual growth against the world average with a zero-growth guide. This dual-line view gives context for relative performance and macroeconomic volatility. The series shows repeated boom-and-bust behaviour, with strong expansions followed by sharp contractions during stress periods. The world line acts as a stable reference and makes Turkey's higher-amplitude cycle clearly visible.

### Exports and Imports

The exports and imports chart uses grouped bars to compare both series across time and includes benchmark reference lines for context. The visual shows imports generally remaining above exports, indicating persistent external imbalance. The grouped format is appropriate because it supports immediate within-year comparison while preserving the temporal trend across the full period.

### Trade Balance

The trade balance chart directly visualises exports minus imports as an area series around a zero baseline. This design highlights deficit persistence because negative values become visually dominant below the reference line. The chart reinforces that imbalance is structural rather than occasional and communicates both direction and depth of the deficit clearly.

### Youth Unemployment by Gender

This chart presents male and female youth unemployment trajectories for Turkey, with world references for context. The multi-series line design is suitable for comparing relative levels and trend behaviour between demographic groups. The key pattern is persistent gender disparity, with female youth unemployment frequently above male unemployment, combined with higher volatility than global benchmarks.

### Inflation Rate

The inflation chart captures year-on-year CPI-based inflation dynamics and makes recent acceleration episodes explicit. A line chart is appropriate because inflation interpretation depends on slope, turning points, and persistence rather than isolated observations. The visual supports the conclusion that inflation is one of the most significant current macroeconomic risks and an important lens for interpreting real-income pressure.

### Turkey Economic Indicators Overview

The overview horizontal bar chart provides a concise cross-indicator comparison of latest available values. The chart is designed for fast comparison across mixed indicators and highlights where stress concentrates in the macroeconomic profile. It complements the time-series visuals by summarising present conditions in one frame while preserving directional cues through color.

---

## Limitations and Validity

Several limitations are explicitly recognised to strengthen analytical credibility. First, indicator series end in different years, so latest-value comparisons are not strict same-year comparisons. Second, trade series currently have a shorter horizon than GDP and unemployment, limiting post-2017 external-balance interpretation. Third, inflation is derived from CPI index changes, which is methodologically sound but should still be interpreted as a modelled metric. Fourth, world benchmarks provide context but are not substitutes for peer-group or causal analysis. The dashboard therefore supports descriptive and comparative interpretation, not causal inference.

---

## Conclusion

This report used the Turkey economic dashboard to examine GDP growth, trade flows, trade balance, youth unemployment, and inflation in a unified analytical framework. The results indicate a country with strong growth potential but notable structural fragility. Growth often compares favourably to world trends, yet persistent trade deficits, gendered youth unemployment pressures, and severe inflation episodes constrain macroeconomic stability. The dashboard approach is effective for communicating these interacting dynamics because it combines summary cues, comparative benchmarks, and time-series evidence in a clear, interpretable sequence.

---

## References

1. World Bank. GDP growth (annual %) [Internet]. Data360; [cited 2026 Apr 7]. Available from: https://data360.worldbank.org/en/indicator/WB_WDI_NY_GDP_MKTP_KD_ZG
2. World Bank. Exports as a percentage of GDP [Internet]. Data360; [cited 2026 Apr 7]. Available from: https://data360.worldbank.org/en/indicator/WEF_GCIHH_EXPGDP
3. World Bank. Imports as a percentage of GDP [Internet]. Data360; [cited 2026 Apr 7]. Available from: https://data360.worldbank.org/en/indicator/WEF_GCIHH_IMPGDP
4. World Bank. Unemployment (%) indicator (Gender Statistics source stream) [Internet]. Data360; [cited 2026 Apr 7]. Available from: https://data360.worldbank.org/en/indicator/WB_GS_SL_UEM_ZS
5. International Monetary Fund. Inflation, average consumer prices, index [Internet]. Data360; [cited 2026 Apr 7]. Available from: https://data360.worldbank.org/en/indicator/IMF_WEO_PCPI
6. McKinney W. Data structures for statistical computing in Python. In: Walt S van der, Millman J, editors. Proceedings of the 9th Python in Science Conference. Austin (TX): SciPy; 2010. p. 56-61.
7. Plotly Technologies Inc. Plotly Python graphing library [Internet]. Montreal: Plotly; [cited 2026 Apr 7]. Available from: https://plotly.com/python/
8. Plotly Technologies Inc. Dash documentation [Internet]. Montreal: Plotly; [cited 2026 Apr 7]. Available from: https://dash.plotly.com/
