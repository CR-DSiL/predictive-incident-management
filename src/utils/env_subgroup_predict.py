"""This function is used to predict the subgroups of env related chnage"""
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
env_subgroup_prediction_model=os.path.join(cwd_path,config['models_dir'],config['env_subgroup_prediction_model'])
env_subgroups_features_names_file=os.path.join(cwd_path,config['models_dir'],config['env_subgroups_features_names'])



def env_subgroup_predict(text):
    #loading the CR corpus used for incident modelling
    Env_subgroup_features_names = pickle.load(open(env_subgroups_features_names_file, 'rb'))
    
    #converting the text data into vectors
    x=CountVectorizer(vocabulary=Env_subgroup_features_names).transform(text)
    
    #creating the features dataframe text vectors i.e.,x
    data=pd.DataFrame(data=x.toarray(),columns=Env_subgroup_features_names)
    
    # loading model & predicting the incidents type
    env_subgroup_model =  pickle.load(open(env_subgroup_prediction_model,'rb'))
    predicted_subgroups=env_subgroup_model.predict(data)
    predicted_subgroup=''.join(predicted_subgroups)

    #data['Subgroups']=predicted_subgroup
    
    return predicted_subgroup