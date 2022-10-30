# Predict Function for project

import pickle


with open('./Models/Dementia-model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)
