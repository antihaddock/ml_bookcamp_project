
# testing the Flask App works locally when predict.py is running
# Test by iterating over all rows of the test dataframe

import requests
import pandas as pd

# Local port test options
#url = 'http://0.0.0.0:9696/predict_outcome'

# Elastic Beanstalk address
#host = 'mlbookcamp-serving.eba-msik3tgu.ap-southeast-2.elasticbeanstalk.com'
#url = f'http://{host}/predict'


df = pd.read_csv('./Data/deployment_test_data.csv')

for i in range(len(df)):
    client = df.iloc[i].to_dict()

    response = requests.post(url, json=client)
    result = response.json()
    print(result)






