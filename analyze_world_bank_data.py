"""Create a small reproducible analysis of life expectancy and GDP per capita.

Data are retrieved from the World Bank Indicators API.  Run:
    python analyze_world_bank_data.py
"""
from pathlib import Path
import requests
import pandas as pd
import matplotlib.pyplot as plt

START_YEAR = 2000
END_YEAR = 2023
API = "https://api.worldbank.org/v2/country/all/indicator/{indicator}?date={start}:{end}&format=json&per_page=20000"
OUT = Path("outputs")
OUT.mkdir(exist_ok=True)


def indicator_frame(indicator: str, value_name: str) -> pd.DataFrame:
    """Download a World Bank indicator and remove aggregate regions."""
    response = requests.get(API.format(indicator=indicator, start=START_YEAR, end=END_YEAR), timeout=30)
    response.raise_for_status()
    payload = response.json()
    rows = payload[1]
    frame = pd.DataFrame(
        {
            "country": [row["country"]["value"] for row in rows],
            "country_code": [row["countryiso3code"] for row in rows],
            "year": [int(row["date"]) for row in rows],
            value_name: [row["value"] for row in rows],
        }
    )
    # Three-letter ISO codes identify countries; blank codes are World Bank aggregates.
    return frame[frame["country_code"].str.len().eq(3)].dropna(subset=[value_name])


life = indicator_frame("SP.DYN.LE00.IN", "life_expectancy")
gdp = indicator_frame("NY.GDP.PCAP.CD", "gdp_per_capita_usd")
data = life.merge(gdp, on=["country", "country_code", "year"], how="inner")
data.to_csv(OUT / "country_year_indicators.csv", index=False)

# Figure 1: cross-country association in the latest year.
latest_year = data["year"].max()
latest = data[data["year"].eq(latest_year)].copy()
fig, ax = plt.subplots(figsize=(9, 6))
ax.scatter(latest["gdp_per_capita_usd"], latest["life_expectancy"], alpha=0.55, color="#1f77b4", edgecolor="white", linewidth=0.4)
ax.set_xscale("log")
ax.set_xlabel("GDP per capita (current US$, log scale)")
ax.set_ylabel("Life expectancy at birth (years)")
ax.set_title(f"Countries with higher GDP per capita generally have longer life expectancy ({latest_year})")
for country in ["China", "United States", "India", "Brazil", "Japan"]:
    row = latest[latest["country"].eq(country)]
    if not row.empty:
        ax.annotate(country, (row.iloc[0]["gdp_per_capita_usd"], row.iloc[0]["life_expectancy"]), xytext=(4, 4), textcoords="offset points", fontsize=8)
fig.tight_layout()
fig.savefig(OUT / "gdp_life_scatter.png", dpi=180)
plt.close(fig)

# Figure 2: time trend for five illustrative countries.
selected = ["China", "United States", "India", "Brazil", "Japan"]
fig, ax = plt.subplots(figsize=(9, 6))
for country in selected:
    subset = data[data["country"].eq(country)].sort_values("year")
    ax.plot(subset["year"], subset["life_expectancy"], marker="o", markersize=2.4, linewidth=1.8, label=country)
ax.set_xlabel("Year")
ax.set_ylabel("Life expectancy at birth (years)")
ax.set_title("Life expectancy rose in the selected countries, 2000-2023")
ax.legend(frameon=False, ncol=2)
ax.grid(axis="y", alpha=0.25)
fig.tight_layout()
fig.savefig(OUT / "life_expectancy_trend.png", dpi=180)
plt.close(fig)

correlation = latest[["life_expectancy", "gdp_per_capita_usd"]].corr(method="spearman").iloc[0, 1]
summary = f"""# Results summary

The analysis contains {len(latest):,} countries or economies with both indicators in {latest_year}.
The Spearman correlation between GDP per capita and life expectancy is {correlation:.2f}.

## Interpretation

Countries with higher GDP per capita generally also have longer life expectancy, but this is an association rather than evidence that income alone causes health outcomes. Countries at similar income levels can have different life expectancy because of health systems, inequality, conflict, education and environmental conditions.

## Limitation

The project uses country-level annual indicators. It cannot show differences within countries, and the latest available year may differ across indicators or countries.
"""
(OUT / "summary.md").write_text(summary, encoding="utf-8")
print(f"Saved {len(data):,} observations and two figures in {OUT}/")
