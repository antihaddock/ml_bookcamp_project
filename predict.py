# Predict Function for project

import pickle
import pandas as pd
from flask import Flask, request, jsonify

with open('./Models/Dementia-model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)




def predict_outcome(df, dv, model):
   # numeric = ['Visit', 'MR Delay', 'Hand', 'Age', 'EDUC', 'SES',
   #    'MMSE', 'CDR', 'eTIV', 'nWBV', 'ASF']
   # categoric = ['M/F']
    #X = df[categoric + numeric].to_dict(orient='rows')
    X = dv.transform([df])
    y_pred = model.predict(X)
    y_pred_prob = model.predict_proba(X)
    return y_pred, y_pred_prob 


#df = pd.read_csv('./Data/deployment_test_data.csv')

#print(predict_outcome(df, dv, model))

app = Flask('Dementia_prediction')


@app.route('/predict_outcome', methods=['POST'])
def predict_outcomes():
    data = request.get_json()
    #df = pd.read_json(data)
    prediction, prediction_prob = predict_outcome(data, dv, model)
    
    result = {
        'Class': prediction.tolist(),
        'probability': prediction_prob.tolist()
    }

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)