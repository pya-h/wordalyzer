import dash
from dash import dcc
from dash import html
import pandas as pd
from models.word import Word, Comment
from dash.dependencies import Input, Output
from termcolor import cprint
from shared import sort_by_y
import os
from threading import Timer


class Dashboard:
    def __init__(self, graph_words_title="", graph_words_type="bar", graph_timeline_type="line",
                 data_name="Unknown") -> None:

        # preprocess data
        # init dash
        self.dashboard = dash.Dash(__name__)
        self.dataset = None
        # design the html layout
        self.marker = '#'
        self.tx, self.ty = self.extract_dataset(0)
        self.x, self.y = sort_by_y(self.tx, self.ty)  # actually dataset is mostly sorted, this line is just to make sure that
        # data is
        # always sorted
        self.graph_words_title = graph_words_title
        self.graph_words_type = graph_words_type
        self.graph_timeline_type = graph_timeline_type
        self.dashboard.layout = self.create_layout()
        data_name = data_name.split('.')
        data_name = ''.join(data_name[:-1])
        self.data_name = data_name
        self.handle_preference_change_event()
        self.handle_marker_change_event()
        #self.handle_timeline_word_select_event()
        self.handle_save_table_event()

    def extract_dataset(self, limit, marker='#'):
        self.dataset = Word.most_used(limit=int(limit), marker=marker)
        if type(self.dataset) is dict:
            return list(self.dataset.keys()), list(self.dataset.values())
        return self.dataset

    def create_layout(self):
        return html.Div(
            className="container",
            children=[
                html.Div(
                    className="title",
                    children=[
                        html.H1(children="Statistics & Timelines"),
                        html.P(
                            children="Here we count all the hashtags that are used among the comments of post viewers:"),
                    ]
                ),
                html.Hr(className="separator"),
                html.Div(
                    children=[
                        html.Div(children="Limit", className="preference-drop-down"),
                        dcc.Dropdown(
                            id="limit-filter",
                            options=[5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
                            value="10",
                            clearable=False,
                            className="preference-drop-down"
                        ),
                        html.Div(children="Marker Character", className="preference-drop-down"),
                        dcc.Dropdown(
                            id="marker-char",
                            options=['None', '#', '$', '!', '@', '%', '^', '&', '*', '(', '_', '-', '~', '.'],
                            value="#",
                            clearable=False,
                            className="preference-drop-down"
                        ),
                    ]
                ),
                dcc.Graph(id="words-chart"),
                html.Hr(className="separator"),
                html.H1(className="score-average", children=f"Score average is {Comment.average()}"),
                dcc.Graph(id="timeline-chart", figure={
                    "data": [
                        {
                            "x": [],
                            "y": [],
                            "type": self.graph_timeline_type,
                        },
                    ],
                    "layout": {"title": ""},
                },
                          ),
                html.Table(id="tableWords", className="table-words", children=[
                    html.Thead(
                        html.Tr(children=[html.Th(
                            html.Button(id="btnSaveTable", className="download-button",
                                        children=html.I(className="fas fa-cloud-upload-alt"))
                        ), html.Th("Word"), html.Th("Iterations"), html.Th("Word"), html.Th("Iterations"), ]),
                    ),
                    html.Tbody(id="tableWordsBody")
                ]),
            ]
        )

    def handle_preference_change_event(self):
        @self.dashboard.callback(
            [Output("words-chart", "figure")],
            [Input("limit-filter", "value"), Input("marker-char", "value")],
        )
        def update_chart_by_new_prefs(limit, marker):
            self.marker = marker if marker and marker.lower() != 'none' else None
            self.x, self.y = self.extract_dataset(limit, marker)
            # Timer(3.0, self.handle_timeline_word_select_event).start()

            return {
                       "data": [
                           {
                               "x": self.x,
                               "y": self.y,
                               "type": self.graph_words_type,
                           },
                       ],
                       "layout": {"title": self.graph_words_title},
                   },

    def handle_marker_change_event(self):
        @self.dashboard.callback(
            [Output("tableWordsBody", "children")],
            [Input("marker-char", "value")],
        )
        def update_table_words_by_marker_change(marker):
            return [self.update_table_words()]

    def handle_timeline_word_select_event(self):
        print("called click handler")
        @self.dashboard.callback(
            [Output("timeline-chart", "figure")],
            [Input(f"btn_word_{i}", "n_clicks") for i in range(len(self.tx))],

        )
        def change_word_timeline(*clicks):
            print(f"word {self.tx[i]} clicked!")
            for i, click in enumerate(clicks):
                if click and self.clicked_state[i] != clicks[i]:
                    self.clicked_state[i] = clicks[i]
                    dataset = Word.timeline(self.tx[i], self.marker)

                    return {
                               "data": [
                                   {
                                       "x": list(dataset.keys()),
                                       "y": list(dataset.values()),
                                       "type": self.graph_timeline_type,

                                   }
                               ],
                               "layout": {"title": f"{self.tx[i]}'s timeline"}
                           },

            return {
                       "data": [
                           {
                               "x": [],
                               "y": [],
                               "type": "line",
                           },
                       ],
                       "layout": {"title": "Select a word to show its timeline:"},
                   },

    def handle_save_table_event(self):
        @self.dashboard.callback(
            Output("btnSaveTable", "n_clicks"),
            [Input("btnSaveTable", "n_clicks")]
        )
        def save_table_as_excel(click):
            if self.dataset:
                data_frame = pd.DataFrame(data=self.dataset, index=["Word", "Iterations"])
                if not os.path.exists('excels'):
                    os.makedirs('excels')

                cprint(f"Successfully exported to excel as 'excels/{self.data_name}.xlsx'", "green")
                data_frame.T.to_excel(f"excels/{self.data_name}.xlsx")

    # now run the server
    def run(self, port=8000, debug=False):
        self.dashboard.run_server("127.0.0.1", port, debug=debug)

    def update_table_words(self):
        tbody = []
        self.tx, self.ty = self.extract_dataset(0, self.marker)
        self.clicked_state = [0 for i in range(len(self.tx))]
        for i in range(0, len(self.tx), 2):
            tbody.append(
                html.Tr(children=[
                    html.Td(), html.Td(html.Button(self.tx[i], id=f"btn_word_{i}",
                                                   n_clicks=0, className="word-button")),
                    html.Td(self.ty[i]),
                    html.Td(html.Button(self.tx[i + 1],
                                        id=f"btn_{self.tx[i + 1]}", n_clicks=0,
                                        className="word-button")),
                    html.Td(self.ty[i + 1])
                ]
                ))
        self.handle_timeline_word_select_event()
        return tbody
