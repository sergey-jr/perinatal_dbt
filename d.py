import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import json

import pandas as pd
import plotly.graph_objs as go


month = {'01': 'Январь', '02': 'Февраль', '03': 'Март', '04': 'Апрель', '05': 'Май', '06': 'Июнь', 
         '07': 'Июль', '08': 'Август', '09': 'Сентябрь', '10': 'Октябрь', '11': 'Ноябрь', '12': 'Декабрь'}
df = []
with open('out.json', encoding='utf-8') as file:
    s = file.read().replace('\n', ',')
    s = '['+s[:-1]+']'
    df = json.loads(s)
    

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



app.layout = html.Div([
        html.Div([
            dcc.Graph(id='graph-with-slider'),
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': i['region'], 'value': i['region']} for i in df],
                value='Российская Федерация'
            ),
            dcc.Dropdown(
                id='year-slider',
                options=[{'label': i, 'value': i} for i in ['2016', '2017', '2018', 'Общая статистика']],
                value='2016'
            )
            ], 
            style={'width': '49%', 'display': 'inline-block'}),
         html.Div([
         dcc.Graph(id='diagram')], style={'width': '49%', 'display': 'inline-block'})
         ])



@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value'),
    Input('crossfilter-xaxis-column', 'value')])
def update_figure(year, region):
    traces = []
    x = []
    y = []
    for i in df:
        if i['region'] == region and i['year'] == year:
            x.append(month[i['month']]),
            y.append(i['death_children']['$numberInt'])
    traces.append(go.Scatter(
        x = x,
        y = y,
        text='Бла',
            mode='markers+lines',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name='хз'
        ))
    
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'type': '-', 'title': 'GDP Per Capita'},
            yaxis={'title': 'Life Expectancy'},
            margin={'l': 80, 'b': 80, 't': 40, 'r': 40},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }
@app.callback(
    Output('diagram', 'figure'),
    [Input('year-slider', 'value'),
    Input('crossfilter-xaxis-column', 'value')])
def update_diagram(year, region):
    traces = []
    if year == 'Общая статистика':
        for i in ['2016', '2017', '2018']:
            x = []
            y = []
            temp = False
            for j in month:
                for z in df:
                    if z['year'] == i and z['region'] == region and z['month'] == j:
                        x.append(month[j])
                        y.append(z['death_children']['$numberInt'])
                        
            print(x, y, i)
            traces.append({
            'x': x,
            'y': y,
            'type': 'bar',
            'name': i
            })
    return{
        'data': traces,
        'layout': {
            'title': 'Besit blet',
            'color': '#7f7f7f',
            'xaxis': dict(color='#7f7f7f')
            }
    }
    
if __name__ == '__main__':
    app.run_server(debug=True)