
from dash import html, Dash, dcc
import navbar
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        navbar.get_navbar(),
        dbc.Container(id="page-content", className="mb-4", fluid=True),
    ]
)

        
if __name__ == "__main__":
    app.run()

