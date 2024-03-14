from dash import Input, Output, callback, html
import PageLayouts as pl
import dashboard as db
import pandas as pd

import dash_bootstrap_components as dbc

csv_file = 'user_input.csv'

home_layout = html.Div(children=[html.H1(children="This is our Home page")])

def get_upload_layout(error=False):
    alerts = html.Div()
    if error:
        alerts = html.Div(dbc.Alert("Invalid Ticker", color="warning"),
                          style={'text-align': 'center'})
    return html.Div(children=[alerts,pl.upload_data_layout()])


def get_dashboard_layout():
    """
    Read saved data from the csv file and use that to 
    retrieve the data that will be used to create the dashboard.

    Return the dashboard that will be created.
    """
    df = db.create_dashboard_data(pd.read_csv(csv_file))
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
        return home_layout
    elif pathname == "/upload_layout":
        return get_upload_layout()
    elif pathname == "/dashboard_layout":
        return get_dashboard_layout()
    else:
        return html.Div(children=[
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognized..."),]
        )
