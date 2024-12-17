###############
## Data Prep ##
###############

## Import packages
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

## Load the processed data
df_account_balances = pd.read_csv('C:\\Users\\kevin\\Documents\\personal\\ynab_wrapped\\intermediate outputs\\account_balances.csv')

## Get unique account types and account names for dropdowns
account_types = df_account_balances['account_type'].unique()
account_names = df_account_balances['account_name'].unique()

## Create Dash app
app = dash.Dash(__name__)


############
## Layout ##
############

app.layout = html.Div([ 

    html.Div([

        ## Title "YNAB Wrapped"
        html.Div(
            'YNAB Wrapped', 
            style={'font-size': '32px', 'font-weight': 'bold', 'padding': '20px', 'textAlign': 'center', 'color': '#333'}
        ),

        ## Box to contain the two dropdowns side by side
        html.Div([ 

            ## Account Type Section
            html.Div([ 
                html.Div('Account Type', style={'font-weight': 'bold', 'textAlign': 'center', 'margin-bottom': '5px'}), 
                dcc.Dropdown(
                    id='account-type-dropdown',
                    options=[{'label': account_type, 'value': account_type} for account_type in account_types],
                    value=account_types[0],  ## Default to the first account type
                    multi=True,
                    style={'width': '100%', 'margin': '10px'}
                ),
            ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'width': '50%', 'padding': '10px'}),  ## Center the dropdown and take half width

            ## Account Name Section
            html.Div([ 
                html.Div('Account Name', style={'font-weight': 'bold', 'textAlign': 'center', 'margin-bottom': '5px'}), 
                dcc.Dropdown(
                    id='account-name-dropdown',
                    options=[{'label': account_name, 'value': account_name} for account_name in account_names],
                    value=[],  ## Default to an empty selection, meaning all accounts
                    multi=True, 
                    style={'width': '100%', 'margin': '10px'}
                ),
            ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'width': '50%', 'padding': '10px'}),  ## Center the dropdown and take half width

        ], style={
            'display': 'flex', 
            'justify-content': 'space-between', 
            'align-items': 'center',  
            'flex-direction': 'row',  
            'background-color': '#f0f8ff',  
            'padding': '20px', 
            'width': '80%',  
            'margin': '0 auto', 
        }),

    ], style={
        'background-color': '#f0f8ff',  
        'border': '2px solid black',  
        'border-radius': '15px', 
        'width': '80%',  
        'margin': '0 auto', 
        'padding': '20px',
    }),

    ## Charts
    html.Div([

        ## Balance Over Time
        html.Div([
            dcc.Graph(id='balance-over-time'),
        ], style={'width': '50%', 'padding': '0 20px'}), 

        ## Transactions Over Time
        html.Div([
            dcc.Graph(id='transactions-over-time'),
        ], style={'width': '50%', 'padding': '0 20px'}),
    ], style={'display': 'flex', 'width': '80%', 'margin': '0 auto', 'justify-content': 'space-between'}),

    ## Callout boxes
    html.Div([

        ## Annual Increase in Balance
        html.Div([
            html.Div(
                'Annual Increase in Balance', 
                style={'font-size': '16px', 'font-weight': 'bold', 'textAlign': 'center', 'margin-bottom': '5px'}
            ),
            html.Div(id='annual-increase', style={'font-size': '20px', 'textAlign': 'center'}),
        ], style={
            'width': '33%', 
            'padding': '10px', 
            'background-color': '#f0f8ff', 
            'border': '2px solid black', 
            'border-radius': '15px', 
            'margin': '0 10px', 
            'textAlign': 'center'
        }),

        ## Annual Percentage Increase
        html.Div([
            html.Div(
                'Annual Percentage Increase', 
                style={'font-size': '16px', 'font-weight': 'bold', 'textAlign': 'center', 'margin-bottom': '5px'}
            ),
            html.Div(id='annual-percentage-increase', style={'font-size': '20px', 'textAlign': 'center'}),
        ], style={
            'width': '33%', 
            'padding': '10px', 
            'background-color': '#f0f8ff', 
            'border': '2px solid black', 
            'border-radius': '15px', 
            'margin': '0 10px', 
            'textAlign': 'center'
        }),

        ## Average Transaction Amount (CY)
        html.Div([
            html.Div(
                'Average Transaction Amount (CY)', 
                style={'font-size': '16px', 'font-weight': 'bold', 'textAlign': 'center', 'margin-bottom': '5px'}
            ),
            html.Div(id='avg-transaction-amount', style={'font-size': '20px', 'textAlign': 'center'}),
        ], style={
            'width': '33%', 
            'padding': '10px', 
            'background-color': '#f0f8ff', 
            'border': '2px solid black', 
            'border-radius': '15px', 
            'margin': '0 10px', 
            'textAlign': 'center'
        }),

    ], style={
        'display': 'flex', 
        'justify-content': 'space-between',
        'width': '80%', 
        'margin': '0 auto',
    }),
])


###############
## Dropdowns ##
###############

@app.callback(
    Output('account-name-dropdown', 'options'),
    [Input('account-type-dropdown', 'value')]
)

def update_account_name_dropdown(account_types):

    ## Ensure account_types is always a list, even if a single account type is selected
    if isinstance(account_types, str):  ## If a single account type is selected as a string
        account_types = [account_types]
    
    ## When account types are selected, get the list of unique account names for those types
    filtered_accounts = df_account_balances[df_account_balances['account_type'].isin(account_types)]['account_name'].unique()
    return [{'label': account_name, 'value': account_name} for account_name in filtered_accounts]


############
## Charts ##
############

@app.callback(
    [Output('transactions-over-time', 'figure'),
     Output('balance-over-time', 'figure')],
    [Input('account-type-dropdown', 'value'),
     Input('account-name-dropdown', 'value')]
)

def update_graph(account_types, account_names):

    ## Ensure account_types is always a list, even if a single account type is selected
    if account_types is None:  ## Default to all account types if None
        account_types = ['All']
    if isinstance(account_types, str):  ## Ensure it's a list if it's a single value
        account_types = [account_types]
    
    if account_names is None or len(account_names) == 0:  ## If no account names are selected, use all account names for the selected account types
        account_names = df_account_balances[df_account_balances['account_type'].isin(account_types)]['account_name'].unique()

    if isinstance(account_names, str):  ## Ensure it's a list if it's a single value
        account_names = [account_names]
    
    ## Filter the data based on the selected account types and account names
    filtered_data_transactions = df_account_balances[ 
        df_account_balances['account_type'].isin(account_types) & 
        df_account_balances['account_name'].isin(account_names)
    ]
    
    ## Aggregate data for Transactions Over Time (sum the number of transactions)
    aggregated_transactions = filtered_data_transactions.groupby(['year'], as_index=False).agg(
        {'number_of_transactions': 'sum'}
    )
    
    ## Aggregate data for Balance Over Time (sum the balances)
    aggregated_balance = filtered_data_transactions.groupby(['year'], as_index=False).agg(
        {'end_of_year_balance': 'sum'}
    )
    
    ## Create Transactions Over Time chart
    figure_transactions = {
        'data': [
            {
                'x': aggregated_transactions['year'],
                'y': aggregated_transactions['number_of_transactions'],
                'type': 'line',
                'hovertemplate': 'Year: %{x}<br>Transactions: %{y}',
                'name': '',  
                'showlegend': False  
            }
        ],
        'layout': {
            'title': 'Transactions Over Time',
            'xaxis': {
                'title': 'Year',
                'tickmode': 'array',
                'tickvals': aggregated_transactions['year'].unique(),
                'ticktext': [str(year) for year in aggregated_transactions['year'].unique()],
                'dtick': 1 
            },
            'yaxis': {
                'title': '',
                'showgrid': True,
                'showline': False  
            },
            'hovermode': 'closest' 
        }
    }

    ## Create Balance Over Time chart
    figure_balance = {
        'data': [
            {
                'x': aggregated_balance['year'],
                'y': aggregated_balance['end_of_year_balance'],
                'type': 'line',
                'hovertemplate': 'Year: %{x}<br>Balance: $%{y:,.2f}',
                'name': '',  
                'showlegend': False 
            }
        ],
        'layout': {
            'title': 'Balance Over Time',
            'xaxis': {
                'title': 'Year',
                'tickmode': 'array',
                'tickvals': aggregated_balance['year'].unique(),
                'ticktext': [str(year) for year in aggregated_balance['year'].unique()],
                'dtick': 1 
            },
            'yaxis': {
                'title': '', 
                'showgrid': True, 
                'showline': False 
            },
            'hovermode': 'closest',
            'hoverlabel': {
                'namelength': 100 
            },
            'template': 'seaborn',
        }
    }

    return figure_transactions, figure_balance


###################
## Callout Boxes ##
###################

@app.callback(
    [
        Output('annual-increase', 'children'),
        Output('annual-percentage-increase', 'children'),
        Output('avg-transaction-amount', 'children')
    ],
    [
        Input('account-type-dropdown', 'value'),
        Input('account-name-dropdown', 'value')
    ]
)

def update_callout_boxes(account_types, account_names):
    
    ## Ensure account_types is always a list
    if isinstance(account_types, str):
        account_types = [account_types]
    
    ## Default to all accounts if no account names are selected
    if not account_names:
        account_names = df_account_balances[df_account_balances['account_type'].isin(account_types)]['account_name'].unique()

    ## Filter data for the selected account types and names
    filtered_data = df_account_balances[df_account_balances['account_type'].isin(account_types) & df_account_balances['account_name'].isin(account_names)]
    
    ## Extract data for balance over time and transactions over time
    filtered_data = filtered_data.groupby(['year']).agg(
        total_balance=('end_of_year_balance', 'sum'),
        total_transactions=('number_of_transactions', 'sum'),
        total_change_in_balance=('change_in_balance', 'sum')
    ).reset_index()

    ## Ensure the dataframe has data for at least two years (current and previous)
    if len(filtered_data) < 2:
        return ("N/A", "N/A", "N/A")  ## If there's insufficient data, return "N/A" for all callouts

    ## Current and Previous Year Balances
    current_year_balance = filtered_data[filtered_data['year'] == filtered_data['year'].max()]['total_balance'].values[0]
    previous_year_balance = filtered_data[filtered_data['year'] == filtered_data['year'].max() - 1]['total_balance'].values[0]
    
    ## Annual Increase in Balance
    annual_increase = current_year_balance - previous_year_balance
    formatted_annual_increase = "${:,.2f}".format(annual_increase)

    ## Annual Percentage Increase
    if previous_year_balance != 0:
        annual_percentage_increase = ((current_year_balance - previous_year_balance) / previous_year_balance) * 100
    else:
        annual_percentage_increase = 0
    formatted_annual_percentage_increase = "{:.2f}%".format(annual_percentage_increase)

    ## Average Transaction Amount (CY)
    current_year_transactions = filtered_data[filtered_data['year'] == filtered_data['year'].max()]['total_transactions'].values[0]
    current_year_change_in_balance = filtered_data[filtered_data['year'] == filtered_data['year'].max()]['total_change_in_balance'].values[0]
    
    ## Error Handling
    if current_year_transactions > 0:
        avg_transaction_amount = current_year_change_in_balance / current_year_transactions
    else:
        avg_transaction_amount = 0
    formatted_avg_transaction_amount = "${:,.2f}".format(avg_transaction_amount)

    return (formatted_annual_increase, formatted_annual_percentage_increase, formatted_avg_transaction_amount)


#################
## Run the app ##
#################

if __name__ == '__main__':
    app.run_server(debug=True)