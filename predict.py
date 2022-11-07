# Predict Function for project
# Takes the pickle file from train.py and utilises this inside a flask server to return a prediction based on data provided to the server

import pickle
import pandas as pd
from flask import Flask, request, jsonify

with open('./Models/Dementia-model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)



# Define a function we can use in the server which takes in data, transforms the data and returns a class and probability
def predict_outcome(df, dv, model):
    X = dv.transform([df])
    y_pred = model.predict(X)
    y_pred_prob = model.predict_proba(X)
    
    return y_pred, y_pred_prob 

app = Flask('Dementia_prediction')

# @app.route(rule="/test", methods=["GET"])
# def test():
#     return 'SERVICE IS UP'

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
    app.run(debug=True, host='0.0.0.0', port=5000)
    