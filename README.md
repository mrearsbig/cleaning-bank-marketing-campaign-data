# Cleaning Bank Marketing Campaign Data

This project cleans and splits data collected during a personal-loan marketing
campaign. The goal is to prepare three CSV files with a consistent structure
for import into PostgreSQL and reuse in future campaigns.

![Project image](docs/image.jpg)

## Project structure

```text
data/
├── raw/
│   └── bank_marketing.csv
└── processed/
    ├── client.csv
    ├── campaign.csv
    └── economics.csv
docs/
└── image.jpg
notebooks/
tests/
src/
└── clean_data.py
```

The original file is preserved unchanged in `data/raw/`. Cleaned results are
generated in `data/processed/`.

## Installation and execution

This project uses `uv` to manage the environment and dependencies:

```bash
uv sync
```

Run the script from the project root:

```bash
uv run python src/clean_data.py
```

The script reads `data/raw/bank_marketing.csv` and writes the three cleaned
files to `data/processed/`.

## Output files

### `client.csv`

Contains the following client fields:

| Column | Type | Description |
| --- | --- | --- |
| `client_id` | integer | Client identifier |
| `age` | integer | Client age in years |
| `job` | object | Job type; periods are replaced with underscores |
| `marital` | object | Marital status |
| `education` | object | Education level; periods become underscores and `unknown` becomes missing |
| `credit_default` | bool | `True` only when the source value is `yes` |
| `mortgage` | bool | `True` only when the source value is `yes` |

### `campaign.csv`

Contains the following campaign fields:

| Column | Type | Description |
| --- | --- | --- |
| `client_id` | integer | Client identifier |
| `number_contacts` | integer | Contact attempts in the current campaign |
| `contact_duration` | integer | Duration of the last contact in seconds |
| `previous_campaign_contacts` | integer | Contact attempts in the previous campaign |
| `previous_outcome` | bool | `True` only when the source value is `success` |
| `campaign_outcome` | bool | `True` only when the source value is `yes` |
| `last_contact_date` | datetime | Date created from `day`, `month`, and the year `2022`, formatted as `YYYY-MM-DD` |

The auxiliary `month` and `day` columns are not included in the final file.

### `economics.csv`

Contains the following economic indicator fields:

| Column | Type | Description |
| --- | --- | --- |
| `client_id` | integer | Client identifier |
| `cons_price_idx` | float | Monthly consumer price index |
| `euribor_three_months` | float | Three-month Euribor rate |

These files are prepared to represent separate client, campaign, and economic
indicator tables in PostgreSQL.

## Validation checklist

After running the script, verify that:

- All three files contain 41,188 records.
- Each file contains exactly the columns documented above.
- Boolean fields contain `True` or `False` values.
- `education` contains no `unknown` values.
- `job` and `education` contain underscores instead of periods.
- `campaign.csv` does not contain the auxiliary `month` or `day` columns.
- `last_contact_date` uses the `YYYY-MM-DD` format and the year `2022`.
