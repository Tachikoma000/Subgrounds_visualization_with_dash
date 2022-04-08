# ==================================================
# Import libraries for this app
import dash
import dash_bootstrap_components as dbc
from dash import html
from millify import millify
from subgrounds.dash_wrappers import Graph
from subgrounds.plotly_wrappers import Figure, Scatter
from klima_subgrounds_demo import sg, protocol_metrics_1year, last_metric, immediate

# This is a single page app

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])


# create the app layout. Nothing too fancy, we just need a way to display the data from the protocol

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Label('Protocol Metrics Demo',
                      style={'font-style': 'normal',
                             'font-weight': '600',
                             'font-size': '64px',
                             'line-height': '96px',
                             'color': '#FFFFFF',
                             }, xs=12, sm=12, md=12, lg=6, xl=6)
        ]),
    ], style={'padding': '10px'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H1('Market Cap'),
                    html.H1('$' +
                            millify(
                                immediate(sg, last_metric.marketCap),
                                precision=2),
                            style={'text-align': 'center'}
                            ),
                ]),
            ]),
        ], xs=12, sm=12, md=12, lg=3, xl=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H1('klima Price'),
                    html.H1('$' +
                            millify(
                                immediate(sg, last_metric.klimaPrice),
                                precision=2),
                            style={'text-align': 'center'}
                            ),
                ]),
            ]),
        ], xs=12, sm=12, md=12, lg=3, xl=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H1('Current APY'),
                    html.H1(
                        millify(
                            immediate(sg, last_metric.currentAPY),
                            precision=2),
                        style={'text-align': 'center'}
                    ),
                ]),
            ]),
        ], xs=12, sm=12, md=12, lg=3, xl=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H1('TVD'),
                    html.H1(
                        millify(
                            immediate(sg, last_metric.totalValueLocked),
                            precision=2),
                        style={'text-align': 'center'}
                    ),
                ]),
            ]),
        ], xs=12, sm=12, md=12, lg=3, xl=3),
    ], style={'padding': '10px'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label('klima Market Cap: '),
                        ]),
                        dbc.Col([
                            millify(
                                immediate(sg, last_metric.marketCap),
                                precision=2)
                        ]),
                    ]),
                ], style={'color': '#FFFFFF',
                          'font-weight': '500',
                          'font-size': '24px',
                          'font-style': 'normal'}),
                dbc.CardBody([
                    Graph(Figure(
                        subgrounds=sg,
                        traces=[
                            Scatter(
                                name='klima Market Cap',
                                x=protocol_metrics_1year.datetime,
                                y=protocol_metrics_1year.marketCap
                            )
                        ],
                        layout={
                            'showlegend': True,
                            'xaxis': {'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white', 'showgrid': False},
                            'yaxis': {'type': 'linear', 'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white',
                                      'title': 'klima Market Cap'},
                            'legend.font.color': 'white',
                            'paper_bgcolor': '#2A2A2A',
                            'plot_bgcolor': '#2A2A2A',
                        }
                    ))
                ]),
            ], style={'height': '100%'}, color='#2A2A2A')
        ], xs=12, sm=12, md=12, lg=6, xl=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label('Staked klima (%)'),
                        ]),
                    ]),
                ], style={'color': '#FFFFFF',
                          'font-weight': '500',
                          'font-size': '24px',
                          'font-style': 'normal'}),
                dbc.CardBody([
                    Graph(Figure(
                        subgrounds=sg,
                        traces=[
                            Scatter(
                                name='staked_supply_percent',
                                x=protocol_metrics_1year.datetime,
                                y=protocol_metrics_1year.staked_supply_percent,
                                mode='lines',
                                line={'width': 0.5, 'color': 'rgb(0, 255, 0)'},
                                stackgroup='one',
                            ),
                            Scatter(
                                name='unstaked_supply_percent',
                                x=protocol_metrics_1year.datetime,
                                y=protocol_metrics_1year.unstaked_supply_percent,
                                mode='lines',
                                line={'width': 0.5, 'color': 'rgb(255, 0, 0)'},
                                stackgroup='one',
                            )
                        ],
                        layout={
                            'title': {'text': 'Staked klima (%)'},
                            'yaxis': {
                                'type': 'linear',
                                'range': [1, 100],
                                'ticksuffix': '%',
                                'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white',
                                'title': 'Staked klima(%)'
                            },
                            'showlegend': True,
                            'xaxis': {'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white', 'showgrid': False},
                            'legend.font.color': 'white',
                            'paper_bgcolor': '#2A2A2A',
                            'plot_bgcolor': '#2A2A2A',
                        }
                    ))
                ]),
            ], style={'height': '100%'}, color='#2A2A2A'),
        ], xs=12, sm=12, md=12, lg=6, xl=6)
    ], style={'padding': '10px'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label('RFV/klima vs klima Price'),
                        ]),
                    ]),
                ], style={'color': '#FFFFFF',
                          'font-weight': '500',
                          'font-size': '24px',
                          'font-style': 'normal'}),
                dbc.CardBody([
                    Graph(Figure(
                        subgrounds=sg,
                        traces=[
                            Scatter(
                                name='Risk-Free Value per klima',
                                x=protocol_metrics_1year.datetime,
                                y=protocol_metrics_1year.rfv_per_klima,
                            ),
                            Scatter(
                                name='klima Price',
                                x=protocol_metrics_1year.datetime,
                                y=protocol_metrics_1year.klimaPrice,
                            ),
                        ],
                        layout={
                            'showlegend': True,
                            'yaxis': {'type': 'linear', 'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white',
                                      'title': 'RFV/klima and klima Price'},
                            'xaxis': {'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white', 'showgrid': False},
                            'legend.font.color': 'white',
                            'paper_bgcolor': '#2A2A2A',
                            'plot_bgcolor': '#2A2A2A',
                        }
                    ))
                ]),
            ], style={'height': '100%'}, color='#2A2A2A'),
        ], xs=12, sm=12, md=12, lg=6, xl=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label('klima Price / RFV per klima (%)'),
                        ]),
                    ]),
                ], style={'color': '#FFFFFF',
                          'font-weight': '500',
                          'font-size': '24px',
                          'font-style': 'normal'}),
                dbc.CardBody([
                    Graph(Figure(
                        subgrounds=sg,
                        traces=[
                            Scatter(
                                name='klima Price / Risk-Free Value per klima (%)',
                                x=protocol_metrics_1year.datetime,
                                y=protocol_metrics_1year.price_rfv_ratio,
                            ),
                        ],
                        layout={
                            'showlegend': True,
                            'yaxis': {'type': 'linear', 'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white',
                                      'title': 'klima Price / RFV per klima (%)'},
                            'xaxis': {'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white', 'showgrid': False},
                            'legend.font.color': 'white',
                            'paper_bgcolor': '#2A2A2A',
                            'plot_bgcolor': '#2A2A2A',
                        }
                    ))
                ]),
            ], style={'height': '100%'}, color='#2A2A2A'),
        ], xs=12, sm=12, md=12, lg=6, xl=6),
    ], style={'padding': '10px'}),
], style={'backgroundColor': '#808080'}, fluid=True)

if __name__ == '__main__':
    app.run_server(debug=True)
