# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import pycountry
import dash_table
from pytrends.request import TrendReq
from collections import OrderedDict

global click_button
global result_trending
global result_anavsdigi
global result_related
click_button = 0


def forCountry(Country, product):
    pytrend = TrendReq()
    ctemp = pycountry.countries.get(name=Country.title())
    if ctemp is None:
        return None
    print(Country.title())
    pytrend.build_payload(kw_list=[product], geo=ctemp.alpha_2)
    interest_by_region_df = pytrend.interest_by_region(resolution='REGION')

    dc = interest_by_region_df.loc[(interest_by_region_df != 0).any(axis=1)]
    column_name = dc.columns.values
    dc = dc.sort_values(by=column_name[0], ascending=False).iloc[0:10]

    return dc


def getRelatedTopic(product):
    pytrend = TrendReq()
    pytrend.build_payload(kw_list=[product])

    related_topics = pytrend.related_topics()
    related_queries = pytrend.related_queries()

    list_of_related_queries = []
    list_of_related_topics = []

    for k in related_queries:
        rel_qarray = related_queries[k]['top']

    if rel_qarray is not None:
        related_queries2 = rel_qarray.loc[:, 'query']
        df = pd.DataFrame(related_queries2, columns=['query'])
        for index, row in df.iterrows():
            list_of_related_queries.append(row["query"])

        for k in related_topics:
            if related_topics[k]['title'] is not None:
                related_tarray = related_topics[k]['title']

        list_of_related_topics = related_tarray.values.tolist()

        return pd.DataFrame(OrderedDict([
            ('related_query', list_of_related_queries),
            ('related_topic', list_of_related_topics),
        ]))


def forCountryMarketing(Country):
    pytrend = TrendReq()
    ctemp = pycountry.countries.get(name=Country.title())
    pytrend.build_payload(kw_list=['Email marketing', 'Radio Advertising', 'Mobile Marketing', 'Television Advertising',
                                   'Facebook Advertisement'],
                          geo=ctemp.alpha_2)  # It can take maximum 5 products in kw_list
    digital_marketing = pytrend.interest_by_region(resolution='REGION')
    pytrend.build_payload(kw_list=['Newspaper Marketing', 'Billboards', 'Bus Shelter Ads', 'Print Ads', 'Fliers'],
                          geo=ctemp.alpha_2)
    analog_marketing = pytrend.interest_by_region(resolution='REGION')

    return digital_marketing, analog_marketing


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[
    html.H1(children="Trend analyzer"),
    html.Div(children="Blue ocean whale sharks"),
    dcc.Input(placeholder="Product", type="text", id="product", value=""),
    dcc.Input(placeholder="Country", type="text", id="country", value=""),
    html.Button("Submit", id="button"),
    html.Div([
        dcc.Tabs(id="tabs", children=[
            dcc.Tab(label="Trending", value="tab-trending", children=[
            ]),
            dcc.Tab(label="Analog vs Digital", value="tab-anavsdig", children=[
            ]),
            dcc.Tab(label="Related Topic", value="tab-related", children=[
            ])
        ]),
        html.Div(id="tabs-content")
    ]),
])


@app.callback(dash.dependencies.Output("tabs-content", "children"), [
    dash.dependencies.Input("button", "n_clicks"),
    dash.dependencies.Input('tabs', 'value'),
    dash.dependencies.Input("product", "value"),
    dash.dependencies.Input("country", "value"),

])
def display_results(n_clicks, tab, product, country):
    global click_button
    global result_trending
    global result_related

    if n_clicks is not None:
        if n_clicks > click_button:
            click_button += 1

            trend = forCountry(country, product)
            if trend is None:
                return html.H1(children="Please enter good country", style={'color': 'red', 'fontSize': 20})
            # digital, analog = forCountryMarketing(country)

            df_related = getRelatedTopic(product)
            n_clicks = 0

            pass
 
            result_trending = dcc.Graph(
                figure={
                    "data": [
                        go.Bar(
                            x=trend[product].index,
                            y=trend[product].values
                        )
                    ]
                }
            )

            result_related = html.Div(children=[
                html.Br(),
                dash_table.DataTable(id="table-related",
                                     style_header={'backgroundColor': 'rgb(30, 30, 30)'},
                                     style_cell={'textAlign': 'center',
                                                 'backgroundColor': 'rgb(50, 50, 50)',
                                                 'color': 'white'
                                                 },
                                     columns=(
                                             [{'id': 'related_topic', 'name': 'Related Topic'}] +
                                             [{'id': 'related_query', 'name': 'Related query'}]
                                     ),
                                     data=df_related.to_dict('rows')
                                     )
            ])

            if tab == 'tab-trending':
                return result_trending
            elif tab == 'tab-anavsdig':
                return html.H3(children="Enter country and click on summit")
            elif tab == 'tab-related':
                return result_related
        else:
            if tab == 'tab-trending':
                return result_trending
            elif tab == 'tab-anavsdig':
                return html.H3(children="Enter country and click on summit")
            elif tab == 'tab-related':
                return result_related
    else:
        if tab == 'tab-trending':
            return html.H3(children="Enter product and country and click on summit")
        elif tab == 'tab-anavsdig':
            return html.H3(children="Enter country and click on summit")
        elif tab == 'tab-related':
            return html.H3(children="Enter product and click on summit")


if __name__ == '__main__':
    app.run_server(debug=True)
