from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import os
import plotly.graph_objects as go


def read_file():
    df = pd.read_excel(os.getcwd()+"\\..\\data\\data.xlsx")
    return df


def sort_data(df):
    indications = df.Indication.unique().tolist()
    pub_types = df.Publication_type.unique().tolist()
    return pub_types, indications


def get_data_indication(row, df, indication):
    pub_type = row['Publication_type']
    row['Count'] = len(df[(df['Publication_type'] == pub_type) & (df['Indication'] == indication)])
    return row


df = read_file()
pub_types, indications = sort_data(df)

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H4('Publication types by Indication'),
    html.Br(),
    dcc.Dropdown(
        id="dropdown",
        options=indications,
        value="Cardiometabolic disease",
        clearable=False,
    ),
    dcc.Graph(id="graph"),
])


@app.callback(
    Output("graph", "figure"),
    Input("dropdown", "value"))
def update_bar_chart(indication):
    result_df = pd.DataFrame()
    result_df['Publication_type'] = pub_types
    result_df = result_df.apply(lambda row: get_data_indication(row, df, indication), axis=1)
    fig = px.bar(result_df, x="Publication_type", y="Count", title="Publication Type", text_auto=True)
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    return fig


if __name__ == '__main__':
    app.run(debug=True)