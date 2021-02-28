from datetime import timedelta
from dash.dependencies import Output, Input
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
from plotly.graph_objs import Layout
from stockstats import StockDataFrame


def sec_transform(i):
    m, s = divmod(i, 60)
    msg = '%02i' % s
    return msg


config = dict({'scrollZoom': True,
               'displaylogo': False})

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        html.H1('Graph updates every minute', style={'textAlign': 'center', 'color': '#7FDBFF'}),
        html.H1(id='live-update-text', style={'textAlign': 'center', 'color': '#7FDBFF'}),
        # for live updating
        dcc.Interval(
            id='interval-component',
            interval=1000,  # 1000 milliseconds
            n_intervals=0),
        html.Div([
            dcc.Graph(id='live_graph', animate=True, style={"height": "100vh"}, config=config),
            dcc.Interval(
                id='interval_component',
                interval=60000,
            ),
        ]),
    ],
    style={"height": "100vh", 'backgroundColor': 'rgb(0,0,0)'}
)


@app.callback(Output('live_graph', 'figure'),
              [Input('interval_component', 'n_intervals')])
def graph_update(n):
    df = pd.read_csv('binance_BTCUSDT_1m.txt')
    df = df.tail(10080)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df['time'] = df['time'] + timedelta(hours=3)
    layout = Layout(plot_bgcolor='rgb(0, 0, 0)')
    layout.xaxis.rangeselector.bgcolor = 'grey'
    layout.hovermode = 'closest'
    graph_candlestick = go.Figure(go.Candlestick(
        x=df['time'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close']
    ), layout=layout)
    graph_candlestick.update_layout(margin=dict(l=50, r=50, b=50, t=20, pad=4))
    graph_candlestick.update_layout(template='plotly_dark')
    graph_candlestick.update_xaxes(showline=True, linewidth=2, linecolor='black', gridcolor='#161616')
    graph_candlestick.update_yaxes(showline=True, linewidth=2, linecolor='black', gridcolor='#161616')
    graph_candlestick.update_xaxes(rangeslider_visible=False)
    graph_candlestick.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=5,
                         label="1m",
                         step='minute',
                         stepmode="backward", ),
                    dict(count=25,
                         label="5m",
                         step="minute",
                         stepmode="todate"),
                    dict(count=75,
                         label="10m",
                         step="minute",
                         stepmode="todate"),
                    dict(count=1,
                         label="1h",
                         step="hour",
                         stepmode="todate"),
                    dict(count=3,
                         label="30m",
                         step="hour",
                         stepmode="todate"),
                    dict(count=1,
                         label="1d",
                         step="day",
                         stepmode="todate"),
                    dict(count=3,
                         label="3d",
                         step="day",
                         stepmode="todate"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=False
            ),
            type="date"
        )
    )
    return graph_candlestick


# call back function
@app.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout(n):
    msg = sec_transform(n)
    return msg

def get_macd(df):
    df = StockDataFrame.retype(df)
    df['macd'] = df.get('macd')


if __name__ == '__main__':
    app.run_server(debug=True)