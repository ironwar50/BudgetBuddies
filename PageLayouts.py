import dash_html_components as html
import dash_core_components as dcc 

def Dashboard(FullName, symbol, LastClose, TrailingPE, ForwardPE, avgAnalystTarget,DCF_ImpliedPrice,PerYGrowth,
              fig, toCompDiv, TradeComps_ImpliedPrices):
    return html.Div([
    html.Div([
        html.Div(
            html.H1(str(FullName) + " (" + str(symbol) + ")", style={'text-align' : 'right', 'margin-right' : '15px'}), 
        ),
        html.Div([
                html.P("Last Close",style={'display' : 'inline-block','margin-left' : '150px'}),
                html.P(LastClose,style={'float' : 'right','display' : 'inline-block','margin-right' : '150px'})
        ]),
        html.Div([
                html.P("P/E",style={'display' : 'inline-block','margin-left' : '150px'}),
                html.P("%0.2f" %TrailingPE,style={'float' : 'right','display' : 'inline-block','margin-right' : '150px'})
        ]),
        html.Div([
                html.P("Forward P/E",style={'display' : 'inline-block','margin-left' : '150px'}),
                html.P("%0.2f" %ForwardPE,style={'float' : 'right','display' : 'inline-block','margin-right' : '150px'})
        ]),
        html.Div([
                html.P("Analyst Target",style={'display' : 'inline-block','margin-left' : '150px'}),
                html.P(avgAnalystTarget,style={'float' : 'right','display' : 'inline-block','margin-right' : '150px'})
        ]),
        html.Br(),
        html.H2("Discounted Cash Flow",style={'display' : 'inline-block','margin-left' : '150px'}),
        html.Div([
            html.P("Current Cash Flow",style={'display' : 'inline-block','margin-left' : '150px'}),
            html.P(DCF_ImpliedPrice['FreeCashFlow'],style={'float' : 'right','display' : 'inline-block','margin-right' : '150px'})
        ]),
        html.Div([
            html.P("Average Yearly Growth",style={'display' : 'inline-block','margin-left' : '150px'}),
            html.P(PerYGrowth,style={'float' : 'right','display' : 'inline-block','margin-right' : '150px'})
        ]),
        html.Div([
            html.P("Year Five Cash Flow",style={'display' : 'inline-block','margin-left' : '150px'}),
            html.P("%0.2f" %DCF_ImpliedPrice['LastYearCashFlow'],style={'float' : 'right','display' : 'inline-block','margin-right' : '150px'})
        ]),
        html.Div([
            html.P("Implied Share Price",style={'display' : 'inline-block','margin-left' : '150px'}),
            html.P("%0.2f" %DCF_ImpliedPrice['ImpliedSharePrice'],style={'float' : 'right','display' : 'inline-block','margin-right' : '150px'})
        ])

    ],style={'textAlign' : 'top' ,'width' : '30%', 'display' : 'inline-block','margin-left' : '450px'}),
    html.Div([
        dcc.Graph(figure=fig),
        html.Div(toCompDiv, style={'float' : 'center'}),
        html.Div([
            html.P("Revenue Share Price: "+str("%0.2f" %TradeComps_ImpliedPrices['revenue_SharePrice']),style={'display' : 'inline-block'}),
            html.P("EBITDA Share Price: "+str("%0.2f" %TradeComps_ImpliedPrices['ebitda_SharePrice']),style={'display' : 'inline-block', 'margin-left' : '50px'}),
            html.P("P/E Share Price: "+str("%0.2f" %TradeComps_ImpliedPrices['netIncome_SharePrice']),style={'display' : 'inline-block', 'margin-left' : '50px'}),
        ],style={'textAlign' : 'center'})
    ],style={'width' : '30%', 'display' : 'inline-block', 'float' : 'right', 'margin-right' : '450px'}),
])