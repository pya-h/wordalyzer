import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

class Dashboard:
    def __init__(self, dataset, x_axis, y_axis, graph_title="", graph_type="bar") -> None:

        # preprocess data
        self.dataset = dataset
        if not x_axis in dataset or not y_axis in dataset:
            raise Exception("Axis field names that you provided are wrong field names; at least one of them doesnt exist in the dataset")
        if x_axis.lower() == "date":
            self.dataset[x_axis] = pd.to_datetime(self.dataset[x_axis], format="%Y-%m-%d")
            self.dataset.sort_values(x_axis, inplace=True)

        # init dash
        self.dashboard = dash.Dash(__name__)

        # design the html layout
        self.dashboard.layout = self.create_layout(self.dataset[x_axis], self.dataset[y_axis], graph_title, graph_type)


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
