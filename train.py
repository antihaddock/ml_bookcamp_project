# training ML model for mid term project

import pandas as pd
import pickle
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer 

# Read in data for exploration and drop unneeded columns
df = pd.read_csv("./Data/oasis_longitudinal.csv")

# Remove unneeded columns
df = df.drop(columns=['Subject ID', 'MRI ID'])

#-------------------- Pre Processing --------------------------------------------------

# Impute mean scores for missing values
mean_value = df['MMSE'].mean()
df['MMSE'] = df['MMSE'].fillna(value=mean_value)

mean_value = df['SES'].mean()
df['SES'] = df['SES'].fillna(value=mean_value)


# -------------- Test Train split and create numeric target variable ------------------

# Test Train split dataset and split into X and Y
X = df.drop(columns=['Group'])
y = df['Group']

# Split into test and train at 60/40
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.6, random_state=1)

# now split into train and validation to give 60/20/20 split
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.5, random_state=1)

# # To use XGBoost Dmatrix we need to label encode our categorical target variabe
# le = LabelEncoder()
# le.fit(y_train)
# y_train_unlabelled = le.transform(y_train)
# y_test_unlabelled = le.transform(y_test)
# y_val_unlabelled = le.transform(y_val)

# ------------------- One Hot Encode using dict vectorizer --------------------------------------
# use dict vectorizer to one hot encode the age variable for X_train, X_test and X_val

numeric = ['Visit', 'MR Delay', 'Hand', 'Age', 'EDUC', 'SES',
       'MMSE', 'CDR', 'eTIV', 'nWBV', 'ASF']
categoric = ['M/F']

# One hot encode the age variable
# One hot encode categoricals using a dict vectorizer
train_dict = X_train[categoric + numeric].to_dict(orient='records')
vectorizer = DictVectorizer(sparse=False)
vectorizer.fit(train_dict)
X_train = vectorizer.transform(train_dict)

# One hot encode test data for model metrics
test_dict = X_test[categoric + numeric].to_dict(orient='records')
X_test = vectorizer.transform(test_dict)

# One hot encode validation data for model metrics
val_dict = X_val[categoric + numeric].to_dict(orient='records')
X_val = vectorizer.transform(val_dict)

# ------------------  Train a XGBoot Model --------------------------------------------------------- 
# We will use the Scikit Learn wrapper of xgb to avoid needing to create matrix and label encode the Y variables

xgparams =  {
 'learning_rate': 0.37304418718359394,
 'max_depth': 23.0,
 'min_child_weight': 14.54228927574913,
 'reg_alpha': 0.07886954783579143,
 'reg_lambda': 0.27914175775055783,
 'objective': 'multi:softmax',
 'num_class': 3,
 'seed': 42}

model = XGBClassifier(xgparams) 
model.fit(X_train, y_train)
#y_pred = model.predict(X_test) 


# ------------- Export trained model to pickle file -------------------------------------------------------

with open('./Models/Dementia-model.bin', 'wb') as f_out:
    pickle.dump((vectorizer, model), f_out)