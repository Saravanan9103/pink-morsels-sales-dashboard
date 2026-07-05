from dash import Dash, html, dcc, Output,Input
import pandas as pd
import plotly.express as px

df = pd.read_csv('formatted_sales_data.csv')
df = df.sort_values(by="date")

app = Dash(__name__)

app.layout = html.Div([
    html.H1(['Pink Morsels Sales Dashboard']),

    html.Div([
        html.Label("Select Region:", style={"fontWeight": "bold", "fontSize": "16px",'display': 'inline','margin-bottom':'20px'}),
        dcc.RadioItems(
            id="region-radio",
            options=[{"label": "All Regions", "value": "All"}] +
                    [{"label": r, "value": r} for r in df["region"].unique()],
            value="All",
            inline=True,
            style={"padding": "10px", "fontSize": "15px",'display': 'inline'}
        )
        ], style={"width": "50%", "margin": "0 auto", "textAlign": "center"}),
    html.Div([
        dcc.Graph(id="sales-graph")
        ], style={"width": "80%", "margin": "auto"})

    ],style={'text-align': 'center','margin-left': '100px','margin-right': '100px'}
    )

@app.callback(
    Output('sales-graph', 'figure'),
    Input('region-radio', 'value')
)
def update_graph(reg):
    if reg == "All":
        plot_df = df
        title = "Sales Over Time (All Regions)"
    else:
        plot_df = df[df["region"] == reg]
        title = f"Sales Over Time - {reg} Region"

    fig = px.line(
        plot_df,
        x="date",
        y="sales",
        color='region',
        title=title,
        markers=True
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Sales ($)",
        template="plotly_white"
    )
    return fig

if __name__ == '__main__':
    app.run(debug=True, port=8051)
