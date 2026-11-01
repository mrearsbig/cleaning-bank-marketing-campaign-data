# Start of the data cleaning script
import pandas as pd
import numpy as np

# Read the raw marketing data
marketing = pd.read_csv('data/raw/bank_marketing.csv')

# Split the data into client, campaign, and economics tables
client = marketing[
    [
        'client_id',
        'age',
        'job',
        'marital',
        'education',
        'credit_default',
        'mortgage'
    ]
].copy()

campaign = marketing[
    [
        'client_id',
        'number_contacts',
        'contact_duration',
        'previous_campaign_contacts',
        'previous_outcome',
        'campaign_outcome',
        'month',
        'day'
    ]
].copy()

economics = marketing[
    [
        'client_id',
        'cons_price_idx',
        'euribor_three_months'
    ]
].copy()

# Clean client data
client['job'] = client['job'].str.replace('.', '_', regex=False)

client['education'] = client['education'].str.replace('.', '_', regex=False)
client['education'] = client['education'].replace('unknown', np.nan)

for col in ['credit_default', 'mortgage']:
    client[col] = client[col] == 'yes'

# Clean campaign outcome data
campaign['previous_outcome'] = campaign['previous_outcome'] == 'success'

campaign['campaign_outcome'] = campaign['campaign_outcome'] == 'yes'

# Create the last contact date using 2022 because the source data has no year column
if 'day' in marketing.columns and 'month' in marketing.columns:
    campaign['last_contact_date'] = pd.to_datetime(
        '2022-' + campaign['month'] + '-' + campaign['day'].astype(str),
        format='%Y-%b-%d',
        errors='coerce'
    )

campaign = campaign[
    [
        'client_id',
        'number_contacts',
        'contact_duration',
        'previous_campaign_contacts',
        'previous_outcome',
        'campaign_outcome',
        'last_contact_date'
    ]
]

# Save the cleaned tables
client.to_csv('data/processed/client.csv', index=False)
campaign.to_csv(
    'data/processed/campaign.csv',
    index=False,
    date_format='%Y-%m-%d'
)
economics.to_csv('data/processed/economics.csv', index=False)