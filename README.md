# Life Expectancy and GDP per Capita

## Research question

Across countries, how are GDP per capita and life expectancy related, and how has life expectancy changed in China, the United States, India, Brazil and Japan since 2000?

## Data source and permissions

The analysis downloads two public World Bank World Development Indicators through the World Bank Indicators API:

- Life expectancy at birth, total (years), indicator `SP.DYN.LE00.IN`
- GDP per capita (current US$), indicator `NY.GDP.PCAP.CD`

World Bank data are available under the Creative Commons Attribution 4.0 International licence. See the [World Bank data licence](https://www.worldbank.org/en/about/legal/terms-of-use-for-datasets) and [API documentation](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation).

## Methods and tools

Python, pandas, matplotlib and requests are used. The script downloads annual values for 2000-2023, keeps country-level records with both indicators, makes a cross-sectional scatter plot for the latest available year, and draws life-expectancy trends for five selected countries. The association is summarised using a Spearman correlation.

## Key findings

In the latest year with data, countries with higher GDP per capita generally have higher life expectancy. The selected countries also show long-run gains in life expectancy, although progress differs by country and period.

## Limitation

This is an observational, country-level analysis. It does not establish causation or describe inequality within countries. The latest data year may also vary across countries and indicators.

## Reproduce the analysis

1. Clone this repository.
2. Create and activate a Python virtual environment (optional but recommended).
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python analyze_world_bank_data.py`
5. Find the processed data, two figures and results summary in `outputs/`.

## Visualisations

After running the script, the following files are created:

- `outputs/gdp_life_scatter.png`
- `outputs/life_expectancy_trend.png`
