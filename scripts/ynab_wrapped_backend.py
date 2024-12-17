###############
## Data Prep ##
###############

## Import packages
import requests
import json
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv(dotenv_path='/Users/kevinroche22/PythonData/ynab_wrapped/.env')

## Set vars
API_KEY = os.getenv('API_KEY')
BUDGET_ID = os.getenv('BUDGET_ID')
BASE_URL = "https://api.ynab.com/v1"

## Set up the headers for authorization
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

## Get all accounts
accounts_url = f"{BASE_URL}/budgets/{BUDGET_ID}/accounts"
response = requests.get(accounts_url, headers=headers)
all_accounts = response.json()['data']['accounts']
all_accounts_df = pd.DataFrame(all_accounts)

## Define account subsets
## String matching is gross but ultimately most appropriate for this use case - revisit in future years to make sure these labels are still applicable.
registered_account_ids = all_accounts_df[all_accounts_df['name'].str.lower().str.contains('rrsp|tfsa|dpsp|lira')]['id'].unique()
non_registered_account_ids = all_accounts_df[all_accounts_df['name'].str.lower().str.contains('non-registered')]['id'].unique()
registered_gains_ids = all_accounts_df[all_accounts_df['name'].str.lower().str.contains('gain')]['id'].unique()
non_registered_gains_ids = all_accounts_df[all_accounts_df['name'].str.lower().str.contains('non-registered gain')]['id'].unique() ## empty... for now.
mortgage_account_ids = all_accounts_df[all_accounts_df['name'].str.lower().str.contains('mortgage')]['id'].unique()
home_value_account_ids = all_accounts_df[all_accounts_df['name'].str.lower().str.contains('house')]['id'].unique()

## Combine all groupings into a dictionary
account_groupings = {
    'Registered': registered_account_ids,
    'Non-Registered': non_registered_account_ids,
    'Registered Gains': registered_gains_ids,
    'Non-Registered Gains': non_registered_gains_ids,
    'Mortgage': mortgage_account_ids,
    'Home Value': home_value_account_ids,
}

## Determine the range of years: 2022 to the current year
current_year = datetime.now().year
years_range = range(2022, current_year + 1)

## Initialize an empty list to store account balances
account_balances = []


######################
## Define Functions ##
######################

## Function to get transactions for an account after a given start date
def get_transactions(account_id):
    response = requests.get(f"{BASE_URL}/budgets/{BUDGET_ID}/accounts/{account_id}/transactions", headers=headers)
    response.raise_for_status()  ## Raise error for bad status codes
    return response.json()["data"]["transactions"]

## Function to manually filter transactions within a date range
def filter_transactions_by_date(transactions, start_date, end_date):
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    filtered_transactions = [
        tx for tx in transactions
        if start_dt <= datetime.strptime(tx['date'], "%Y-%m-%d") <= end_dt
    ]
    return filtered_transactions


##################
## Calculations ##
##################

## Loop through each account group
for group_name, account_ids in account_groupings.items():

    ## Print group name
    print(f"Currently looking at {group_name}.")

    ## Skip groups that have no account IDs
    if len(account_ids) == 0:
        print(f"Skipping {group_name} as it has no accounts.")
        continue  ## Skip to the next grouping if no accounts are in this one

    ## Loop through accounts within grouping 
    for account_id in account_ids:

        ## Fetch the account details from the YNAB API
        account = next(acc for acc in all_accounts if acc['id'] == account_id)

        ## Get all transactions for the account
        transactions = get_transactions(account_id)
        
        ## Loop through the years from the first year we had the budget to the current year
        for year in years_range:

            ## Print year
            print(f"Making calculations for {account['name']} in {year}.")
            
            ## Define the start and end date. Budget was started in 2022, so this loops through each year and calculates using all transactions from 2022 to the year in question.
            start_date = "2022-01-01"
            end_date = f"{year}-12-31"
            transactions_over_timeframe = filter_transactions_by_date(transactions, start_date, end_date)
            
            ## Calculate the balance for the end of the year (sum of filtered transactions)
            balance_end_of_year = sum(tx['amount'] for tx in transactions_over_timeframe) / 1000
            number_of_transactions = len(transactions_over_timeframe)
            
            ## Store the balances along with the account, group, and year info
            account_balances.append({
                'account_type': group_name,
                'account_name': account['name'],
                'year': year,
                'number_of_transactions_in_timeframe': number_of_transactions,
                'end_of_year_balance': balance_end_of_year
            })

## Convert the results to a DataFrame for better readability
df_account_balances = pd.DataFrame(account_balances)

## Calculate the actual number of transactions and balance changes
df_account_balances['number_of_transactions'] = df_account_balances.groupby('account_name')['number_of_transactions_in_timeframe'].diff().fillna(df_account_balances['number_of_transactions_in_timeframe']).astype(int)
df_account_balances = df_account_balances.drop(columns=['number_of_transactions_in_timeframe'])
df_account_balances['change_in_balance'] = df_account_balances.groupby('account_name')['end_of_year_balance'].diff().fillna(0)


##################
## Write to csv ##
##################

df_account_balances.to_csv('/Users/kevinroche22/PythonData/ynab_wrapped/intermediate outputs/account_balances.csv', index=False)