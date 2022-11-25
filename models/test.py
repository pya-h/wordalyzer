import pandas as pd

def testme():
    data = pd.read_csv('models/avocado.csv')
    print(data)
    for row in data:
        print(row)

if __name__ == "__main__":
        testme()
