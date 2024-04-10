from dash import Input, Output, callback, html
import PageLayouts as pl
import dashboard as db
import pandas as pd

import dash_bootstrap_components as dbc

csv_file = 'user_input.csv'

def database_layout():
    db_layout = pl.database_table_layout()
    if(db_layout == -1):
        return home_layout(-2)
    return db_layout

def home_layout(error=0):
    alerts = html.Div()
    if error == -1:
        alerts = html.Div(dbc.Alert("Enter Data First", color="warning"),
                          style={'text-align': 'center'})
    elif error == -2:
        alerts = html.Div(dbc.Alert("Database Empty", color="warning"),
                          style={'text-align': 'center'})
    return html.Div(children=[alerts,pl.create_homepage()])


def get_upload_layout(error=0):
    """
    Check for errors. Create alert add to upload_layout. 
    Retrieve upload page. 

    Return upload layout    
    """
    alerts = html.Div()
    if error == -1:
        alerts = html.Div(dbc.Alert("Missing Value", color="warning"),
                          style={'text-align': 'center'})
    elif error == -2:
        alerts = html.Div(dbc.Alert("Duplicate in Tickers to Compare", color="warning"),
                          style={'text-align': 'center'})
    elif error == -3:
        alerts = html.Div(dbc.Alert("Duplicate with Target Ticker", color="warning"),
                          style={'text-align': 'center'})
    elif error == -4:
        alerts = html.Div(dbc.Alert("Invalid Target Ticker", color="warning"),
                          style={'text-align': 'center'})
    elif error == -5:
        alerts = html.Div(dbc.Alert("Invalid Ticker in Tickers to Compare", color="warning"),
                          style={'text-align': 'center'})
    elif error == -6:
        alerts = html.Div(dbc.Alert("Enter Data First", color="warning"),
                          style={'text-align': 'center'})
    return html.Div(children=[alerts,pl.upload_data_layout()])


def get_dashboard_layout():
    """
    Read saved data from the csv file and use that to 
    retrieve the data that will be used to create the dashboard.

    Return the dashboard that will be created if no error.
    If error return back to upload_layout. 
    """
    try:
        df = db.create_dashboard_data(pd.read_csv(csv_file))
    except FileNotFoundError:
        return get_upload_layout(-6)
    if df['error']:
        return get_upload_layout(df['error'])
    return pl.create_dashboard(df)


def get_navbar():
    """
    This creates navigation links for visiting other local pages
    within the project.
    """
    return dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("Data upload", href="/upload_layout")),
            dbc.NavItem(dbc.NavLink("Dashboard", href="/dashboard_layout")),
            dbc.NavItem(dbc.NavLink("Database", href="/database_layout")),
        ],
        brand="Budget Buddies",
        color="dark",
        dark=True,
        className="mb-2",
    )


@callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    """
    Callback method checks whether the passed in pathname is valid and returns
    the component that will display the page associated with the pathname.

    Args:
        pathname (string): A pathname to one of the local pages within the project.

    Returns:
        dash component: The component for visiting the pathname.
    """
    if pathname == "/":
        return home_layout()
    elif pathname == "/upload_layout":
        return get_upload_layout()
    elif pathname == "/dashboard_layout":
        return get_dashboard_layout()
    elif pathname == "/database_layout":
        return database_layout()
    else:
        return html.Div(children=[
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognized..."),]
        )
