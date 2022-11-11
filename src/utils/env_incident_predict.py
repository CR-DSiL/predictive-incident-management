""" This function predicts the env related incindet type"""
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
env_incident_prediction_model=os.path.join(cwd_path,config['models_dir'],config['env_incident_prediction_model'])


def env_incident_predict(Text):
    
    
    #loading the Env vocabulary used for incident modelling
    vocab = ["sql","server","integration","load balance","notification","db","database","webserver","website","share","connectivity"]
        
    #converting the text data into vectors
    cv = CountVectorizer(stop_words='english',vocabulary=vocab)
    x= cv.transform([Text])
    
    #creating the features dataframe text vectors i.e.,x
    data=pd.DataFrame(data=x.toarray(),columns=vocab)
    
    
    # loading model & predicting the incidents type
    env_incident_model =  pickle.load(open(env_incident_prediction_model,'rb'))
    predicted_incident=env_incident_model.predict(data)
    predicted_incident_type=''.join(predicted_incident)
    #data['Incidents']=predicted_incident_type
    
    return predicted_incident_type