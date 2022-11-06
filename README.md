Mid term project for 2022 ML Bookcamp course.
Written by Ryan Gallagher

Data utilised in MRI and Alzeimhers dataset from Kaggle
https://www.kaggle.com/datasets/jboysen/mri-and-alzheimers


## How to use this Repo ##

### Exploratory Data Analysis ###
Data is stored in the `Data` directory. `oasis_longitudinal.csv` is the data utiulised by `notebook.ipynb` for exploratory analysis and modelling. `train.py` also utilises this data to train the XGboost model used in project.  In `train.py` a XGBoost model is trained utilising the hyperopts library to find optium hyperparameters for the model.

The test data created in the test/train/validation split is saved as `deployment_test_data.csv`  which can be used to sev data to the model.


### Interacting with the model ###

You can utilise the `test_serve_flask_app.py` in interact with the trained model. The ways you may interact with the model via `test_serve_flask_app.py` are as follows:
 1. From the command line simply run `python predict.py` to utise the flask to service the model. In a separate window run `python test_serve_flask_app.py` to run the model via flaks
 2.  call `gunicorn --bind 0.0.0.0:9696  predict_outcome:app` from the command line to run this model via gunicorn (linux only)
 
### Using Pip Env and Pip File ###
A pipfile is provided for this repo. To install dependencies call `pipenv install`. To activate the environment call `pipenv shell`. 


 ### Interacting via docker container ###

 A dockerfile is available in this repo to allow a docker image to be created for serving this model. To run this model within dovker
 1. Call `docker build -t mlbookcamp-project .` to build the docker image locally. Once the docker image is built locally calling `docker run -it --rm -p  5000:5000  mlbookcamp-project` will allow interaction with the docker container for  `test_serve_flask_app.py`. Ensure you do not have a flask or gunicorn server running locally if you wish to interact with the model via docker.

 ### Deployment to Elastic Beanstalk ###

 This model and its docker container is deployed to Elastic Beanstalk. This container on EB can be interacted with by uncommenting line 12 & 13 in `test_serve_flask_app.py` to point this script to the deployed container location.

 If you would like to deploy this model to your own EB instance you will need the following steps
 1. Call `eb init -p docker -r ap-southeast-2  mlbookcamp-serving` to intialise an elastic beanstalk instance for deployment. Replace the -r region with whatever your preferred region is.  Call ` eb create mlbookcamp-env` to finish the creation of the EB instance.
 2. You may run the EB instance locally for testing via `eb local run --port 9696`
 3. To deploy this container to your own EB account `eb create mlbookcamp-serving` will deploy the docker contaiiner.