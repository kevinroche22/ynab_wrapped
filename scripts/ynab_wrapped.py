###############
## Data Prep ##
###############

## Import packages
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_daq as daq
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

## Load the processed data
df_account_balances = pd.read_csv('/Users/kevinroche22/PythonData/ynab_wrapped/intermediate outputs/account_balances.csv')

## Get unique account types and account names for dropdowns
account_types = df_account_balances['account_type'].unique()
account_names = df_account_balances['account_name'].unique()

## Create Dash app with dark mode theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])


############
## Layout ## 
############

app.layout = html.Div([ 

    html.Div([

        ## Title "YNAB Wrapped"
        html.Div(
            'YNAB Wrapped', 
            style={'font-size': '32px', 'font-weight': 'bold', 'padding': '20px', 'textAlign': 'center', 'color': '#fff'}
        ),

        ## Box to contain the toggle and two dropdowns in a row
        html.Div([ 

            ## Hide Numbers Section
            html.Div([ 
                html.Div('Hide Numbers', style={'font-weight': 'bold', 'textAlign': 'center', 'margin-bottom': '5px', 'color': '#fff'}),  
                daq.ToggleSwitch(
                    id='toggle-dots',
                    label='',
                    color='#7CDD7E',
                    value=True,  ## Initially hide the numbers
                    style={'width': '100%', 'margin': '0px', 'padding': '0px 110px'}
                ),
            ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'width': '30%', 'padding': '10px'}),

            ## Account Type Section
            html.Div([ 
                html.Div('Account Type', style={'font-weight': 'bold', 'textAlign': 'center', 'margin-bottom': '5px', 'color': '#fff'}),  
                dcc.Dropdown(
                    id='account-type-dropdown',
                    options=[{'label': account_type, 'value': account_type} for account_type in account_types],
                    value=account_types[0],  ## Default to the first account type
                    multi=True,
                    style={
                        'width': '100%',
                        'margin': '0px',
                        'backgroundColor': '#444', 
                        'color': '#444',
                        'border-radius': '5px', 
                        'border': '1px solid #666' 
                    }
                ),
            ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'width': '30%', 'padding': '10px'}),

            ## Account Name Section
            html.Div([ 
                html.Div('Account Name', style={'font-weight': 'bold', 'textAlign': 'center', 'margin-bottom': '5px', 'color': '#fff'}), 
                dcc.Dropdown(
                    id='account-name-dropdown',
                    options=[{'label': account_name, 'value': account_name} for account_name in account_names],
                    value=[],  ## Default to an empty selection, meaning all accounts
                    multi=True, 
                    style={
                        'width': '100%',
                        'margin': '0px',
                        'backgroundColor': '#444',
                        'color': '#444',
                        'border-radius': '5px', 
                        'border': '1px solid #666' 
                    }
                ),
            ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'width': '30%', 'padding': '10px'}),

        ], style={ 
            'display': 'flex', 
            'justify-content': 'space-between',  
            'align-items': 'flex-start',  
            'flex-direction': 'row',  
            'background-color': '#333', 
            'padding': '10px', 
            'width': '80%', 
            'margin': '0 auto', 
            'box-sizing': 'border-box',
        }),

    ], style={
        'background-color': '#333',
        'border': '2px solid #666',
        'border-radius': '15px',
        'width': '80%',
        'margin': '15px auto 0',
        'padding': '10px',
        'box-sizing': 'border-box'}
),

    ## Charts
    html.Div([

        ## Balance Over Time
        html.Div([ 
            dcc.Graph(id='balance-over-time', style={'width': '75vh', 'height': '55vh'}), 
        ], style={'width': '50%', 'padding': '0 20px'}), 

        ## Changes Over Time
        html.Div([ 
            dcc.Graph(id='changes-over-time', style={'width': '75vh', 'height': '55vh'}), 
        ], style={'width': '50%', 'padding': '0 20px'}), 

    ], style={'display': 'flex', 'width': '80%', 'margin': '0 auto', 'justify-content': 'space-between'}),

    ## Callout boxes
    html.Div([

        ## Annual Increase in Balance
        html.Div([ 
            html.Div(
                'Annual Increase in Balance', 
                style={'font-size': '16px', 'font-weight': 'bold', 'textAlign': 'center', 'margin-bottom': '5px', 'color': '#fff'}
            ),
            html.Div(id='annual-increase', style={'font-size': '20px', 'textAlign': 'center', 'color': '#fff'}),
        ], style={ 
            'width': '33%', 
            'padding': '10px', 
            'background-color': '#444', 
            'border': '2px solid #666',  
            'border-radius': '15px', 
            'margin': '0 10px', 
            'textAlign': 'center'
        }),

        ## Annual Percentage Increase
        html.Div([ 
            html.Div(
                'Annual Percentage Increase', 
                style={'font-size': '16px', 'font-weight': 'bold', 'textAlign': 'center', 'margin-bottom': '5px', 'color': '#fff'}
            ),
            html.Div(id='annual-percentage-increase', style={'font-size': '20px', 'textAlign': 'center', 'color': '#fff'}),
        ], style={ 
            'width': '33%', 
            'padding': '10px', 
            'background-color': '#444', 
            'border': '2px solid #666',  
            'border-radius': '15px', 
            'margin': '0 10px', 
            'textAlign': 'center'
        }),

        ## Average Transaction Amount (CY)
        html.Div([ 
            html.Div(
                'Average Transaction Amount (CY)', 
                style={'font-size': '16px', 'font-weight': 'bold', 'textAlign': 'center', 'margin-bottom': '5px', 'color': '#fff'}
            ),
            html.Div(id='avg-transaction-amount', style={'font-size': '20px', 'textAlign': 'center', 'color': '#fff'}),
        ], style={ 
            'width': '33%', 
            'padding': '10px', 
            'background-color': '#444', 
            'border': '2px solid #666',  
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
    if isinstance(account_types, str):
        account_types = [account_types]
    
    ## When account types are selected, get the list of unique account names for those types
    filtered_accounts = df_account_balances[df_account_balances['account_type'].isin(account_types)]['account_name'].unique()
    return [{'label': account_name, 'value': account_name} for account_name in filtered_accounts]


############
## Charts ##
############

@app.callback(
    [
        Output('balance-over-time', 'figure'),
        Output('changes-over-time', 'figure')
    ],
    [
        Input('account-type-dropdown', 'value'),
        Input('account-name-dropdown', 'value'),
        Input('toggle-dots', 'value')
    ]
)

def update_charts(account_types, account_names, hide_numbers):
    
    ## Ensure account_types is always a list
    if isinstance(account_types, str):
        account_types = [account_types]
    
    ## Default to all accounts if no account names are selected
    if not account_names:
        account_names = df_account_balances[df_account_balances['account_type'].isin(account_types)]['account_name'].unique()

    ## Filter data based on selected account types and names
    filtered_data = df_account_balances[df_account_balances['account_type'].isin(account_types) & df_account_balances['account_name'].isin(account_names)]
    
    ## Prepare data for the balance-over-time chart
    balance_over_time_data = filtered_data.groupby(['year'])['end_of_year_balance'].sum().reset_index()
    changes_over_time_data = filtered_data.groupby(['year'])['change_in_balance'].sum().reset_index()
    changes_over_time_data = changes_over_time_data[changes_over_time_data['year'] != 2022]

    ## Apply formatting only when 'Hide Numbers' is toggled
    if hide_numbers:

        ## Keep numeric values but hide them in the hovertext and Y-Axis formatting
        balance_over_time_data['formatted_balance'] = '$•••'
        changes_over_time_data['formatted_change'] = '$•••'
        
        ## Y-Axis tick labels should show "$•••" but still scale correctly
        yaxis_tickvals = balance_over_time_data['year']
        yaxis_ticktext_balance = ['$•••'] * len(yaxis_tickvals)
        yaxis_ticktext_changes = ['$•••'] * len(yaxis_tickvals)

    else:

        ## Apply currency formatting for hovertext
        balance_over_time_data['formatted_balance'] = balance_over_time_data['end_of_year_balance'].apply(lambda x: f"${x:,.2f}")
        changes_over_time_data['formatted_change'] = changes_over_time_data['change_in_balance'].apply(lambda x: f"${x:,.2f}")
        
        ## For Y-Axis, apply numeric currency formatting
        yaxis_tickvals = balance_over_time_data['year']
        yaxis_ticktext_balance = [f"${x:,.0f}" for x in balance_over_time_data['end_of_year_balance']]
        yaxis_ticktext_changes = [f"${x:,.0f}" for x in changes_over_time_data['change_in_balance']]
    
    ## Balance Over Time Chart
    balance_over_time_figure = {
        'data': [
            go.Scatter(
                x=balance_over_time_data['year'],
                y=balance_over_time_data['end_of_year_balance'], 
                mode='lines+markers',
                name='Balance Over Time',
                text=balance_over_time_data['formatted_balance'], 
                hoverinfo='text' 
            )
        ],
        'layout': go.Layout(
            title='Balance Over Time',
            plot_bgcolor='#272b30', 
            paper_bgcolor='#272b30', 
            font=dict(color='white'),
            xaxis={
                'title': 'Year',
                'tickmode': 'array',
                'tickvals': balance_over_time_data['year'].unique(),
                'ticktext': [str(year) for year in balance_over_time_data['year'].unique()],
                'dtick': 1,
                'tickfont': dict(color='white') 
            },
            yaxis={
                'tickvals': balance_over_time_data['end_of_year_balance'], 
                'ticktext': yaxis_ticktext_balance,  
                'tickformat': '$,0.0f',  
                'tickfont': dict(color='white') 
            }
        )
    }
    
    ## Changes Over Time Chart
    changes_over_time_figure = {
        'data': [
            go.Bar(
                x=changes_over_time_data['year'],
                y=changes_over_time_data['change_in_balance'], 
                name='Changes in Balance',
                text=changes_over_time_data['formatted_change'], 
                textposition = "none",
                hoverinfo='text' 
            )
        ],
        'layout': go.Layout(
            title='Changes in Balance Over Time',
            plot_bgcolor='#272b30',  
            paper_bgcolor='#272b30',  
            font=dict(color='white'),  
            xaxis={
                'title': 'Year',
                'tickmode': 'array',
                'tickvals': changes_over_time_data['year'].unique(),
                'ticktext': [str(year) for year in changes_over_time_data['year'].unique()],
                'dtick': 1,
                'tickfont': dict(color='white') 
            },
            yaxis={
                'tickvals': changes_over_time_data['change_in_balance'],
                'ticktext': yaxis_ticktext_changes, 
                'tickformat': '$,0.0f',
                'tickfont': dict(color='white') 
            }
        )
    }
    
    return balance_over_time_figure, changes_over_time_figure


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
        Input('account-name-dropdown', 'value'),
        Input('toggle-dots', 'value') 
    ]
)

def update_callout_boxes(account_types, account_names, hide_numbers):

    ## Ensure account_types is always a list
    if isinstance(account_types, str):
        account_types = [account_types]
    
    ## Default to all accounts if no account names are selected
    if not account_names:
        account_names = df_account_balances[df_account_balances['account_type'].isin(account_types)]['account_name'].unique()

    ## Filter data for the selected account types and names
    filtered_data = df_account_balances[df_account_balances['account_type'].isin(account_types) & df_account_balances['account_name'].isin(account_names)]
    
    ## Group by year to perform calculations
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
    formatted_annual_increase = "${:,.2f}".format(annual_increase) if not hide_numbers else "$•••"

    ## Annual Percentage Increase
    if previous_year_balance != 0:
        annual_percentage_increase = ((current_year_balance - previous_year_balance) / previous_year_balance) * 100
    else:
        annual_percentage_increase = 0
    formatted_annual_percentage_increase = "{:.2f}%".format(annual_percentage_increase) if not hide_numbers else "$•••"

    ## Average Transaction Amount (CY)
    current_year_transactions = filtered_data[filtered_data['year'] == filtered_data['year'].max()]['total_transactions'].values[0]
    current_year_change_in_balance = filtered_data[filtered_data['year'] == filtered_data['year'].max()]['total_change_in_balance'].values[0]
    
    ## Error Handling
    if current_year_transactions > 0:
        avg_transaction_amount = current_year_change_in_balance / current_year_transactions
    else:
        avg_transaction_amount = 0
    formatted_avg_transaction_amount = "${:,.2f}".format(avg_transaction_amount) if not hide_numbers else "$•••"

    return (formatted_annual_increase, formatted_annual_percentage_increase, formatted_avg_transaction_amount)


if __name__ == '__main__':
    app.run_server(debug=True)