import pandas as pd
from models.test import testme
from views.dashboard import Dashboard

#testme()

data = pd.read_csv('models/avocado.csv')
data = data.query('type == "conventional" and region == "Albany"')

_ = Dashboard(data, "Date", "AveragePrice", graph_title = "Number of #")
_.show()
# localhost:8050
