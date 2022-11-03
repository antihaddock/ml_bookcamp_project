
# testing the Flask App works locally when predict.py is running
# Test by iterating over all rows of the test dataframe

import requests
import pandas as pd

#url = 'http://172.26.3.210:9696/predict_outcome'
url = 'http://127.0.0.1:5000/predict_outcome'

df = pd.read_csv('./Data/deployment_test_data.csv')

for i in range(len(df)):
    client = df.iloc[i].to_dict()

    response = requests.post(url, json=client)
    result = response.json()
    print(result)






