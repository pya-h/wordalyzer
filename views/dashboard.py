import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from models.word import Word
from dash.dependencies import Input, Output, State
from shared import find_diffrenet

class Dashboard:
    def __init__(self, graph_title="", graph_type="bar") -> None:

        # preprocess data
        # init dash
        self.dashboard = dash.Dash(__name__)

        # design the html layout
        x, y = self.extract_dataset(0)

        self.dashboard.layout = self.create_layout(x, y)

        self.auto_update_on_limit_change(graph_title, graph_type)

    def extract_dataset(self, limit):
        self.dataset = Word.most_used(limit=int(limit))
        if type(self.dataset) is dict:
            return (list(self.dataset.keys()), list(self.dataset.values()))
        return self.dataset


    def create_layout(self, x, y):
        tbody = []
        self.clicked_state = [0 for i in range(len(x))]
        for i in range(len(x)):
            tbody.append(html.Tr(children=[html.Td(html.Button(x[i], id=f"btn_{x[i]}", n_clicks=0)), html.Td(y[i])]))
            #add call back for btn_word_{i}
        @self.dashboard.callback(
            Output("div_result", "children"),
            [Input(f"btn_{x[i]}", "n_clicks") for i in range(len(x))],

        )
        def change_word_timeline(*clicks):
            result = ""
            for i, click in enumerate(clicks):
                if click and self.clicked_state[i] != clicks[i]:
                    result = x[i]
            # update previous to current
            for i, click in enumerate(clicks):
                self.clicked_state[i] = clicks[i]
            return result

        return html.Div(
                    className="container",
                    children=[
                        html.Div(
                            className="title",
                            children=[
                                html.H1(children="Words Statistics"),
                                html.P(children="Here we count all the hashtags that are used among the comments of post viewers:"),
                            ]
                        ),
                        html.Hr(className="separator"),
                        html.Div(
                            children=[
                                html.Div(children="Limit", className="limit-drop-down"),
                                dcc.Dropdown(
                                    id="limit-filter",
                                    options=[5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
                                    value="10",
                                    clearable=False,
                                    className="limit-drop-down"
                                ),
                            ]
                        ),
                        dcc.Graph(id="words-chart"),
                        html.Hr(className="separator"),
                        html.Table(className="table-words", children=[
                            html.Thead(
                                html.Tr(children=[html.Th("Word"), html.Th("Iterations")]),
                            ),
                            html.Tbody(tbody)
                        ]),
                        html.Div(id="div_result", children="test")
                    ]
                )

    def auto_update_on_limit_change(self, graph_title, graph_type):
        @self.dashboard.callback(
            [Output("words-chart", "figure")],
            [Input("limit-filter", "value")]
        )
        def update_chart(limit):
            x, y = self.extract_dataset(limit)
            return {
                "data": [
                    {
                        "x": x,
                        "y": y,
                        "type": graph_type,
                    },
                ],
                "layout": {"title": graph_title},
            },

    # now run the server
    def run(self, debug=True):
        self.dashboard.run_server(debug=debug)
