from dash import Input, Output, callback
from dash import html
import PageLayouts as pl
import dashboard as db

import dash_bootstrap_components as dbc

home_layout = html.Div(children=[html.H1(children="This is our Home page")])

data_upload_layout = html.Div(children=[
    pl.upload_data_layout()
])

dashboard_layout = html.Div(children=[
    db.create_dashboard()
])

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
        return data_upload_layout
    elif pathname == "/dashboard_layout":
        return dashboard_layout
    else:
        return html.Div(children=[
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognized..."),]
        )