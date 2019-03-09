# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import pycountry
from pytrends.request import TrendReq


def forCountry(Country, product):
    pytrend = TrendReq()
    ctemp=pycountry.countries.get(name=Country.title())
    print(Country.title())
    pytrend.build_payload(kw_list=[product], geo=ctemp.alpha_2)
    interest_by_region_df = pytrend.interest_by_region(resolution='REGION')

    related_topics = pytrend.related_topics()
    related_queries = pytrend.related_queries()

    dc = interest_by_region_df.loc[(interest_by_region_df != 0).any(axis=1)]
    column_name = dc.columns.values
    dc = dc.sort_values(by=column_name[0],ascending= False).iloc[0:10]
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

    return dc, list_of_related_queries, list_of_related_topics


def forCountryMarketing(Country):
    pytrend = TrendReq()
    ctemp = pycountry.countries.get(name=Country.title())
    pytrend.build_payload(kw_list=['Email marketing', 'Radio Advertising', 'Mobile Marketing', 'Television Advertising', 'Facebook Advertisement'], geo=ctemp.alpha_2) #It can take maximum 5 products in kw_list
    digital_marketing = pytrend.interest_by_region(resolution='REGION')
    pytrend.build_payload(kw_list=['Newspaper Marketing', 'Billboards', 'Bus Shelter Ads', 'Print Ads','Fliers'],geo=ctemp.alpha_2)
    analog_marketing = pytrend.interest_by_region(resolution='REGION')

    return digital_marketing , analog_marketing


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children="Trend analyzer"),
    html.Div(children="Blue ocean whale sharks"),
    dcc.Input(placeholder="Product", type="text", value="", id="product"),
    dcc.Input(placeholder="Country", type="text", value="", id="country"),
    html.Button("Submit", id="button"),
    html.Div(id="result")#, style={"columnCount": 2}),
])


@app.callback(dash.dependencies.Output("result", "children"), [
    dash.dependencies.Input("product", "value"),
    dash.dependencies.Input("country", "value"),
])
def display_results(product, country):
    trend, table_1, table_2 = forCountry(country, product)
    digital, analog = forCountryMarketing(country)
    pass

    return dcc.Graph(
            figure={
                "data": [
                    go.Bar(
                        x=trend[product].index,
                        y=trend[product].values
                    )
                ]
            }
        )



if __name__ == '__main__':
    app.run_server(debug=True)
