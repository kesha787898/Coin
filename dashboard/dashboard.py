import os

import dash
import dash_html_components as html
import plotly.graph_objects as go
import dash_core_components as dcc
from dash.dependencies import Input, Output
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("postgresql://fezjdnvz:TuwZaCWfkD2xz3QTVhf1wOSQ6DZ9hh3x@abul.db.elephantsql.com/fezjdnvz",
                       echo=True, future=True)
df = pd.read_sql('prices', engine.connect())
df['weighted_price'] = df['price'] * df['tradable_quantity']
df = df.groupby(pd.Grouper(key='created_at', freq='60s')).agg({'price': ['min', 'max'],
                                                               'tradable_quantity': ['sum'],
                                                               'weighted_price': ['sum']})

df.columns = [' '.join(col).strip().replace(' ', '_') for col in df.columns.values]
df = df.reset_index(level=0)
df = df.rename(columns={"tradable_quantity_sum": "price_quantity"})

df['weighted_price_mean'] = df['weighted_price_sum'] / df['price_quantity']
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(id='parent', children=[
    html.H1(id='H1', children='Styling using html components', style={'textAlign': 'center',
                                                                      'marginTop': 40, 'marginBottom': 40}),

    dcc.Dropdown(id='dropdown',
                 options=[
                     {'label': 'weighted_price_mean', 'value': 'weighted_price_mean'},
                     {'label': 'price_min', 'value': 'price_min'},
                     {'label': 'price_max', 'value': 'price_max'},
                     {'label': 'price_quantity', 'value': 'price_quantity'},
                 ],
                 value='price_min'),
    dcc.Graph(id='bar_plot')
])


@app.callback(Output(component_id='bar_plot', component_property='figure'),
              [Input(component_id='dropdown', component_property='value')])
def graph_update(dropdown_value):
    fig = go.Figure([go.Scatter(x=df['created_at'], y=df[f"{dropdown_value}"],
                                line=dict(color='firebrick', width=4))
                     ])

    fig.update_layout(title='Stock prices over time',
                      xaxis_title='Dates',
                      yaxis_title='Values'
                      )
    return fig


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8050))
    app.run(host='0.0.0.0', port=port)
