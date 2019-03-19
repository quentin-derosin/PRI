# -*- coding: utf-8 -*-
import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_table
import pandas as pd
import pycountry
from pytrends.request import TrendReq
from collections import OrderedDict
import numpy


class utilGraph:
    def __init__(self, index, value):
        self.index = index
        self.value = value


class Analog_or_digital:
    def __init__(self, name, data, index):
        self.name = name
        self.data = data
        self.index = index


class Graphs:
    trending = None
    anavsdigi = None
    related = None
    analysis_print = None
    click_button = 0


def forCountry(country, product):
    pytrend = TrendReq()
    ctemp = pycountry.countries.get(name=country.title())
    if ctemp is None:
        return None
    print(country.title())
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

        if len(list_of_related_queries) > 8 and len(list_of_related_topics) > 8:
            list_of_related_topics = list_of_related_topics[0:8]
            list_of_related_queries = list_of_related_queries[0:8]
        elif len(list_of_related_topics) > len(list_of_related_queries):
            list_of_related_topics = list_of_related_topics[0:len(list_of_related_queries)]
        elif len(list_of_related_topics) < len(list_of_related_queries):
            list_of_related_queries = list_of_related_queries[0:len(list_of_related_topics)]

        return pd.DataFrame(OrderedDict([
            ('related_query', list_of_related_queries),
            ('related_topic', list_of_related_topics),
        ]))


def forCountryMarketing(Country):
    pytrend = TrendReq()
    list_analog_name = ['Email marketing', 'Radio Advertising', 'Mobile Marketing', 'Television Advertising',
                        'Facebook Advertisement']
    list_digital_name = ['Newspaper Marketing', 'Billboards', 'Bus Shelter Ads', 'Print Ads', 'Fliers']
    ctemp = pycountry.countries.get(name=Country.title())
    pytrend.build_payload(kw_list=list_analog_name, geo=ctemp.alpha_2)  # It can take maximum 5 products in kw_list
    digital_marketing = pytrend.interest_by_region(resolution='REGION')
    pytrend.build_payload(kw_list=list_digital_name, geo=ctemp.alpha_2)
    analog_marketing = pytrend.interest_by_region(resolution='REGION')

    list_analog_data = [
        analog_marketing['Newspaper Marketing'].mean(),
        analog_marketing['Billboards'].mean(),
        analog_marketing['Bus Shelter Ads'].mean(),
        analog_marketing['Print Ads'].mean(),
        analog_marketing['Fliers'].mean()
    ]

    list_digital_data = [
        digital_marketing['Email marketing'].mean(),
        digital_marketing['Radio Advertising'].mean(),
        digital_marketing['Mobile Marketing'].mean(),
        digital_marketing['Television Advertising'].mean(),
        digital_marketing['Facebook Advertisement'].mean(),
    ]

    digital = utilGraph(list_digital_name, list_digital_data)
    analog = utilGraph(list_analog_name, list_analog_data)
    return digital, analog


graph = Graphs()

VALID_USERNAME_PASSWORD_PAIRS = [
    ['quentin', 'derosin'],
    ['amaury', 'julien']
]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.layout = html.Div(children=[
    html.Header(children=[
        html.Div([
            html.H1(children="Trend analyzer"),
            html.Img(src="/assets/logo_epita.png", className="logo_epita"),
            html.H3(children="by Quentin DEROSIN & Amaury JULIEN")], className="title-text"),
        html.Div([
            html.P([html.Strong("Trend Analyzer"), " is a powerful tool made for marketers."]),
            html.P("It has been developed to help professionals making decision when marketing a product."),
            html.H3("How does it work ?"),
            html.P("First of all, you to select the product to be marketed and the target country"),
            html.P("Then our algorithms will provide you useful information such as :"),
            html.Ul([html.Li(
                "- Trending : How much this product is searched in Google for each region of the given country"),
                html.Li("- Analog / Digital : Is the product more searched with analog or digital ways"),
                html.Li(
                    "- Related topics : This tab also suggests related products to make the study more accurate.")]),
            html.P(
                "Finally, our artificial intelligence gives you the best approach to market your product based on previous results.")
        ]),
        html.Div([html.A("Give it a try !", href='#search', className="search_button")], className="center")
    ]),
    html.Div([
        html.H2("Search engine"),
        dcc.Input(placeholder="Product", type="text", value="", id="product", className="four columns",
                  style={'margin-left': '0px'}),
        dcc.Input(placeholder="Country", type="text", value="", id="country", className="four columns"),
        html.Button("Submit", id="button")], id="search", className="row"),
    html.Div([
        html.H2("Results"),
        dcc.Tabs(id="tabs", children=[
            dcc.Tab(label="Trending", value="tab-trending", children=[
            ]),
            dcc.Tab(label="Analog vs Digital", value="tab-anavsdig", children=[
            ]),
            dcc.Tab(label="Related Topics", value="tab-related", children=[
            ])
        ]),
        html.Div(id="tabs-content")], id='results'),
    html.Div([
        dcc.Interval(
            id='interval-component',
            interval=1 * 1000,  # in milliseconds
            n_intervals=0
        ),

        html.Div(id='analysis')
    ]),
    html.Footer([
        html.P("Quentin DEROSIN - Amaury JULIEN - EPITA PRI 2019")
    ])
], id="body")


@app.callback(dash.dependencies.Output("tabs-content", "children"), [
    dash.dependencies.Input("button", "n_clicks"),
    dash.dependencies.Input('tabs', 'value'),
    dash.dependencies.Input("product", "value"),
    dash.dependencies.Input("country", "value"),

])
def display_results(n_clicks, tab, product, country):
    if n_clicks is not None:
        if n_clicks > graph.click_button:
            graph.click_button += 1

            trend = forCountry(country, product)
            if trend is None:
                return html.H1(children="Please enter good country",
                               style={'color': 'red', 'fontSize': 20, 'text-align': 'center'}, className="align-center")

            analog, digital = forCountryMarketing(country)

            df_related = getRelatedTopic(product)

            pass

            graph.trending = dcc.Graph(
                figure={
                    "data": [
                        go.Bar(
                            x=trend[product].index,
                            y=trend[product].values
                        )
                    ]
                }
            )

            graph.related = html.Div([
                html.Br(),
                dash_table.DataTable(id="table-related",
                                     # style_table={'width': '90#'},
                                     style_cell={'textAlign': 'center',
                                                 'minWidth': '512px', 'width': '512px', 'maxWidth': '512px',
                                                 'overflow': 'hidden',
                                                 'textOverflow': 'ellipsis',
                                                 },
                                     columns=[
                                         {'id': 'related_topic', 'name': 'Related Topic'},
                                         {'id': 'related_query', 'name': 'Related query'}],
                                     css=[{
                                         'selector': '.dash-cell div.dash-cell-value',
                                         'rule': 'display: inline; white-space: inherit; overflow: '
                                                 'inherit; text-overflow: inherit; '
                                     }],
                                     data=df_related.to_dict('rows')

                                     )
            ])

            graph.anavsdigi = dcc.Graph(
                figure={
                    "data": [
                        go.Bar(
                            x=analog.index,
                            y=analog.value,
                            name='Analog'
                        ),
                        go.Bar(
                            x=digital.index,
                            y=digital.value,
                            name='Digital'
                        )
                    ]
                }
            )
            if analog.value[numpy.argmax(analog.value)] >= digital.value[numpy.argmax(digital.value)]:
                best = Analog_or_digital("analog", analog, numpy.argmax(analog.value))
                bad = Analog_or_digital("digital", digital, numpy.argmax(digital.value))

            else:
                best = Analog_or_digital("digital", digital, numpy.argmax(digital.value))
                bad = Analog_or_digital("analog", analog, numpy.argmax(analog.value))

            graph.analysis_print = html.Div([
                html.H2("Analysis"),
                html.P("In " + country.upper() + ", to market " + product.upper() +
                       ", we advise you tu use " + best.name.upper() + " marketing because" +
                       " the proportion of " + best.data.index[best.index].upper() +
                       ", which is the most representative field, is " + str(round(best.data.value[best.index])) + "%."),
                html.P("On the contrary, " + bad.name.upper() + " is only represented with " +
                       bad.data.index[bad.index].upper() + " at " + str(round(bad.data.value[bad.index])) + " %"),
                html.Div([html.A("Search something else !", href='#search', className="search_button")], className="center")])
            if tab == 'tab-trending':
                return graph.trending
            elif tab == 'tab-anavsdig':
                return graph.anavsdigi
            elif tab == 'tab-related':
                return graph.related
        else:
            graph.analysis_print = None
            if tab == 'tab-trending':
                return graph.trending
            elif tab == 'tab-anavsdig':
                return graph.anavsdigi
            elif tab == 'tab-related':
                return graph.related
    else:
        graph.analysis_print = None
        return html.H3(children="Enter product & country and click on submit to get results.", className="align-center")


@app.callback(dash.dependencies.Output('analysis', 'children'),
              [dash.dependencies.Input('interval-component', 'n_intervals')])
def print_analysis(n):
    return graph.analysis_print


if __name__ == '__main__':
    app.run_server(debug=True)
