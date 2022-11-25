import pandas as pd

def load_excel(filename='models/avocado.csv'):
    data = pd.read_csv(filename)
    data = data.query('type == "conventional" and region == "Albany"')
    return data


def testme():
    data = pd.read_csv('models/avocado.csv')
    print(data)
    for row in data:
        print(row)
