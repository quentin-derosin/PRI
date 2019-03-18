# -*- coding: utf-8 -*-
import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_table
from tests.server import Server
from tests.graphs import Graphs

graph = Graphs()

VALID_USERNAME_PASSWORD_PAIRS = [
    ['quentin', 'derosin'],
    ['amaury','julien']
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
            html.P([html.Strong("Trend Analyzer")," is a powerful tool made for marketers."]),
            html.P("It has been developed to help professionals making decision when marketing a product."),
            html.H3("How does it work ?"),
            html.P("First of all, you to select the product to be marketed and the target country"),
            html.P("Then our algorithms will provide you useful information such as :"),
            html.Ul([html.Li("- Trending : How much this product is searched in Google for each region of the given country"),
                     html.Li("- Analog / Digital : Is the product more searched with analog or digital ways"),
                     html.Li("- Related topics : This tab also suggests related products to make the study more accurate.")]),
            html.P("Finally, our artificial intelligence gives you the best approach to market your product based on previous results.")
        ]),
        html.Div([html.A("Give it a try !", href='#search', className="search_button")], className="center")
    ]),
    html.Div([
        html.H2("Search engine"),
        dcc.Input(placeholder="Product", type="text", value="", id="product", className="four columns", style={'margin-left': '0px'}),
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
        html.H2("Analysis"),
        html.P("//To fill with custom analysis")
    ], id="analysis"),
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

            trend = Server.forCountry(country, product)
            if trend is None:
                return html.H1(children="Please enter good country", style={'color': 'red', 'fontSize': 20})

            digital, analog = Server.forCountryMarketing(country)

            df_related = Server.getRelatedTopic(product)

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

            graph.related = html.Div(children=[
                html.Br(),
                dash_table.DataTable(id="table-related",
                                     style_cell={'textAlign': 'center',
                                                 },
                                     columns=(
                                             [{'id': 'related_topic', 'name': 'Related Topic'}] +
                                             [{'id': 'related_query', 'name': 'Related query'}]
                                     ),
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

            if tab == 'tab-trending':
                return graph.trending
            elif tab == 'tab-anavsdig':
                return graph.anavsdigi
            elif tab == 'tab-related':
                return graph.related
        else:
            if tab == 'tab-trending':
                return graph.trending
            elif tab == 'tab-anavsdig':
                return graph.anavsdigi
            elif tab == 'tab-related':
                return graph.related
    else:
        if tab == 'tab-trending':
            return html.H3(children="Enter product and country and click on submit")
        elif tab == 'tab-anavsdig':
            return html.H3(children="Enter country and click on submit")
        elif tab == 'tab-related':
            return html.H3(children="Enter product and click on submit")


if __name__ == '__main__':
    app.run_server(debug=True)
