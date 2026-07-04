from IPython import display
from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px

df = pd.read_csv('data/formatted_sales_data.csv')
print(df.head())
df = df.sort_values("date")
app = Dash(__name__)

fig = px.line(df, x='date', y='sales')

app.layout = html.Div([
    html.H1(['Pink Morsels Sales Dashboard']),
    html.Div([dcc.Graph(
        id='sales-graph', figure=fig
    )]
    )
],style={'text-align': 'center','margin-left': '100px','margin-right': '100px'}
)

if __name__ == '__main__':
    app.run(debug=True, port=8051)
