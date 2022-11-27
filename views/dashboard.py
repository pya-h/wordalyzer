import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

class Dashboard:
    def __init__(self, dataset, graph_title="", graph_type="bar") -> None:

        # preprocess data
        self.dataset = dataset
        # init dash
        self.dashboard = dash.Dash(__name__)

        # design the html layout
        x, y = self.extract_dataset()

        self.dashboard.layout = self.create_layout(x, y, graph_title, graph_type)


    def extract_dataset(self):
        if type(self.dataset) is dict:
            return (list(self.dataset.keys()), list(self.dataset.values()))
        return self.dataset


    def create_layout(self, x, y, title, type='bar'):
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
                        dcc.Graph(
                            figure={
                                "data": [
                                    {
                                        "x": x,
                                        "y": y,
                                        "type": type,
                                    },
                                ],
                                "layout": {"title": title},
                            },
                        ),
                    ]
                )

    # now run the server
    def run(self, debug=True):
        self.dashboard.run_server(debug=debug)
