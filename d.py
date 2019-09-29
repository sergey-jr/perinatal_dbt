import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import os
import glob

import pandas as pd
import plotly.graph_objs as go

INPUT_DIR = os.path.join(os.getcwd(), 'data\main')

li = []
for year in os.listdir(INPUT_DIR):
    load_data_dir = os.path.join(INPUT_DIR, year)
    all_files = glob.glob(load_data_dir + "\*.csv")
    for filename in all_files:
        df = pd.read_csv(filename, engine='python', encoding='utf-8', index_col=None,
                         header=0)
        li.append(df)

data = pd.concat(li, axis=0, ignore_index=False)

df = data[['region', 'birth', 'death_children', 'marriage', 'divorce', 'year', 'month']]
regions = df['region'].unique()
month = {'01': 'Январь', '02': 'Февраль', '03': 'Март', '04': 'Апрель', '05': 'Май', '06': 'Июнь',
         '07': 'Июль', '08': 'Август', '09': 'Сентябрь', '10': 'Октябрь', '11': 'Ноябрь', '12': 'Декабрь'}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='crossfilter-xaxis-column',
                    options=[{'label': i, 'value': i} for i in regions],
                    value='Белгородская область'
                )
            ], style={'width': '69%', 'display': 'inline-block'}),
            html.Div([
                dcc.Dropdown(
                    id='year-slider',
                    options=[{'label': i, 'value': i} for i in ['2016', '2017', '2018']],
                    value='2016'
                )
            ], style={'width': '30%', 'display': 'inline-block'}),
        ], ),
        html.Div([
            dcc.Graph(id='graph-with-slider')],style={'display': 'inline-block'})
    ], style={'width': '40%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(id='diagram')], style={'width': '40%', 'display': 'inline-block'}),
    html.Div([
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='side_1',
                    options=[{'label': 'Детская смертность', 'value': 'death_children'},
                             {'label': 'Кол-во браков', 'value': 'marriage'},
                             {'label': 'Кол-во разводов', 'value': 'divorce'}],
                    value='marriage')
            ], style={'width': '30%', 'display': 'inline-block'}),
            html.Div([
                dcc.Dropdown(
                    id='side_2',
                    options=[{'label': 'Детская смертность', 'value': 'death_children'},
                             {'label': 'Кол-во браков', 'value': 'marriage'},
                             {'label': 'Кол-во разводов', 'value': 'divorce'}],
                    value='divorce')
                ], style={'width': '30%', 'display': 'inline-block'})
            ]),
            dcc.Graph(id='indicator-graphic')
            ], style={'width': '80%', 'padding': '40px 40px 40px 40px'}),
        html.Div([
            dcc.Slider(
                id='month--slider',
                min=1,
                max=12,
                value=12,
                marks={int(i): month[i] for i in month},
                step=None),
    ], style={'width': '49%', 'padding': '40px 40px 40px 40px'}),
    ])


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value'),
     Input('crossfilter-xaxis-column', 'value')])
def update_figure(year, region):
    traces = []
    x = list(month.values())
    y = df.loc[(df['year'] == int(year)) & (df['region'] == region), 'death_children'].values
    traces.append(go.Scatter(
        x=x,
        y=y,
        text=f'Детская смертность {region}',
        mode='markers+lines',
        opacity=0.7,
        marker={
            'size': 15,
            'line': {'width': 0.5, 'color': 'white'}
        },
        name='Детская смертность в разные месяцы'
    ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'type': '-', 'title': 'Месяц'},
            yaxis={'title': 'Детская смертность'},
            margin={'l': 80, 'b': 80, 't': 40, 'r': 40},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }


@app.callback(
    Output('diagram', 'figure'),
    [Input('crossfilter-xaxis-column', 'value')])
def update_diagram(region):
    x = list(month.values())
    y_1 = df.loc[(df['year'] == 2016) & (df['region'] == region), 'death_children'].values
    y_2 = df.loc[(df['year'] == 2017) & (df['region'] == region), 'death_children'].values
    y_3 = df.loc[(df['year'] == 2018) & (df['region'] == region), 'death_children'].values
    traces = []
    traces.append({
        'x': x,
        'y': y_1,
        'type': 'bar',
        'name': '2016'
    })
    traces.append({
        'x': x,
        'y': y_2,
        'type': 'bar',
        'name': '2017'
    })
    traces.append({
        'x': x,
        'y': y_3,
        'type': 'bar',
        'name': '2018'
    })

    return {
        'data': traces,
        'layout': {
            'title': 'Общая статистика',
            'color': '#7f7f7f',
            'xaxis': dict(color='#7f7f7f'),
            'barmode': 'stack',
            'colorway': ["#7a4c99", "#6f8bc7", "65c1ee"],
            'hovermode': "closest",
            'opacity': 0.7

        }
    }


@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('side_1', 'value'),
     Input('side_2', 'value'),
     Input('year-slider', 'value'),
     Input('month--slider', 'value')])
def update_graph(feat_1, feat_2, year, month):
    dff = df.loc[(df['year'] == int(year)) & (df['month'] == month)]

    return {
        'data': [go.Scatter(
            x=dff[feat_1],
            y=dff[feat_2],
            text=dff['region'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': feat_1
            },
            yaxis={
                'title': feat_2
            },
            margin={'l': 80, 'b': 0, 't': 40, 'r': 40},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
