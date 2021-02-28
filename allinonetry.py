from datetime import timedelta
from dash.dependencies import Output, Input
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
from plotly.graph_objs import Layout
from stockstats import StockDataFrame as Sdf
from plotly.subplots import make_subplots


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
            dcc.Graph(id='live_graph1', animate=True, style={"height": "100vh"}, config=config),
            dcc.Interval(
                id='interval_component1',
                interval=60000,
            ),
            dcc.Graph(id='live_graph2', animate=True, style={"height": "100vh"}, config=config),
            dcc.Interval(
                id='interval_component2',
                interval=60000,
            ),
            dcc.Graph(id='live_graph3', animate=True, style={"height": "100vh"}, config=config),
            dcc.Interval(
                id='interval_component3',
                interval=60000,
            ),
            dcc.Graph(id='live_graph4', animate=True, style={"height": "100vh"}, config=config),
            dcc.Interval(
                id='interval_component4',
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

    stock = Sdf.retype(df)
    df['signal'] = stock['macds']
    df['macd'] = stock['macd']
    df['hist'] = stock['macdh']

    rsi_6 = stock["rsi_6"]
    rsi_12 = stock["rsi_12"]

    df = df.tail(10080)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df['time'] = df['time'] + timedelta(hours=3)
    layout = Layout(plot_bgcolor='rgb(0, 0, 0)')
    layout.xaxis.rangeselector.bgcolor = 'grey'
    layout.hovermode = 'closest'
    fig = make_subplots(shared_xaxes=True, rows=4, cols=1, row_heights=[0.6, 0.15, 0.3, 0.3],
                        vertical_spacing=0.009, horizontal_spacing=0.009)
    fig['layout']['margin'] = {'l': 30, 'r': 10, 'b': 50, 't': 25}
    graph_candlestick = fig.add_trace(go.Candlestick(
        x=df['time'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'], name='candlestick'), row=1, col=1)
    fig.update_xaxes(rangeslider_visible=False)
    ap = fig.add_trace(go.Scatter(name='macd', x=df['time'], y=df['macd'], line=dict(color='blue')), row=3, col=1)
    ap1 = fig.add_trace(go.Scatter(name='signal', x=df['time'], y=df['signal'], line=dict(color='orange')), row=3,
                        col=1)
    ap2 = fig.add_trace(go.Bar(name='histogram', x=df['time'], y=df['hist'], marker_color='green'), row=2, col=1)
    ap2.update_layout(barmode='stack')
    fig.update_layout(template='plotly_dark')
    ap3 = fig.add_trace(go.Scatter(x=df['time'], y=list(rsi_6), name="RSI 6 Day"), row=4, col=1)
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
    return graph_candlestick, ap, ap1, ap2, ap3


# call back function
@app.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout(n):
    msg = sec_transform(n)
    return msg


if __name__ == '__main__':
    app.run_server(debug=True)