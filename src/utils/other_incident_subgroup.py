''' This file contains function to predict the subgroups of other incident types'''
import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
import yaml
import os


# Load config file
with open('config/config.yaml') as file:
  config= yaml.safe_load(file)
  #print(config)

#Get current working dir
cwd_path=os.getcwd()

# Different required paths
Other_subgroup_features_names=os.path.join(cwd_path,config['models_dir'],config['Other_subgroup_features_names'])
other_subgroup_prediction_model=os.path.join(cwd_path,config['models_dir'],config['other_subgroup_prediction_model'])


def predict_subgroup(text,impact,incident_type):

    #loading the CR corpus used for incident modelling
    features_names_subgroups = pickle.load(open(Other_subgroup_features_names, 'rb'))

    # converting text data into numerical
    cv = CountVectorizer(stop_words='english',vocabulary=features_names_subgroups)
    x = cv.transform([text])

    #creating the features dataframe text vectors i.e.,x
    x2=pd.DataFrame.sparse.from_spmatrix(x,columns=features_names_subgroups)
    x2['Impact'] = impact
    x2['Incident'] = incident_type
    x2.replace(['4 - Low','3 - Medium','2 - High','1 - Major'],[4,3,2,1],inplace=True)
    x2.replace(['Capacity Incident','Capacity Incidents','Service Request Incident','Service Request Incidents'],[1,1,2,2],inplace=True)

    # loading model & predicting the incidents type
    pickled_model = pickle.load(open(other_subgroup_prediction_model, 'rb'))
    predicted_subgroup_type=pickled_model.predict(x2)
    # predicted_subgroup_type
    predicted_subgroup_type=str(predicted_subgroup_type[0])
    return predicted_subgroup_type