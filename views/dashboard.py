import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

# preprocess data
data = pd.read_csv('../models/avocado.csv')
data = data.query('type == "conventional" and region == "Albany"' )
print(data)
data["Date"] = pd.to_datetime(data['Date'], format="%Y-%m-%d")
data.sort_values("Date", inplace=True)

# init dash
dashboard = dash.Dash(__name__)

# design the html layout
dashboard.layout = html.Div( style={
        "fontSize": "20px",
        "marginTop": "10px"
    },
    children=[
        html.Div(
            style={
                'margin':'2rem',
                "textAlign": "center"
            },
            children=[
                html.H1(children="Words Statistics"),
                html.P(children="Here we count all the hashtags that are used among the comments of post viewers:"),
            ]
        ),
        html.Hr(style={"border": "2px dashed lightgrey", "margin": "100px"}),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["Date"],
                        "y": data["AveragePrice"],
                        "type": "bar",
                    },
                ],
                "layout": {"title": "Number of Hashtags"},
            },
        ),
        # dcc.Graph(
        #     figure={
        #         "data": [
        #             {
        #                 "x": data["Date"],
        #                 "y": data["Total Volume"],
        #                 "type": "lines",
        #             }
        #         ],
        #         "layout": {"title": "Number of whatever"}
        #     },
        # )
    ]
)

# now run the server
if __name__ == "__main__":
    dashboard.run_server(debug=True)
