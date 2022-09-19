# Import Libs
#data handling
import pandas as pd
import numpy as np
import re

import yaml
import os

#data vectorization
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

#model loading
import pickle

#handle the text data
import re
import string


#lemmatization for text
import spacy
nlp = spacy.load('en_core_web_sm')

# to ingore the warning messages
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.filterwarnings("ignore")

# Load config file
with open('config/config.yaml') as file:
  config= yaml.safe_load(file)
  #print(config)

#Get current working dir
cwd_path=os.getcwd()

# Different required paths
cr_stop_words_file=os.path.join(cwd_path,config['models_dir'],config['cr_stop_words_file'])
cr_incident_type_features_names_file=os.path.join(cwd_path,config['models_dir'],config['cr_incident_type_features_names'])
cr_incident_prediction_model_file=os.path.join(cwd_path,config['models_dir'],config['cr_incident_prediction_model'])
cr_impact_dict=config['cr_impact_dict']
cr_subgroups_features_names_file=os.path.join(cwd_path,config['models_dir'],config['cr_subgroups_features_names'])
cr_incident_types_dict=config['cr_incident_types_dict']
cr_capcity_subgroup_prediction_model=os.path.join(cwd_path,config['models_dir'],config['cr_capcity_subgroup_prediction_model'])
cr_network_subgroup_prediction_model=os.path.join(cwd_path,config['models_dir'],config['cr_network_subgroup_prediction_model'])
cr_cloud_subgroup_prediction_model=os.path.join(cwd_path,config['models_dir'],config['cr_cloud_subgroup_prediction_model'])
cr_dataset_file_path=os.path.join(cwd_path,config['data_dir'],config['cr_dataset_file'])
similar_incident_count=config['similar_incident_count']


## Load the stopwords 
stopwords = pickle.load(open(cr_stop_words_file, 'rb'))


## Text pre-processing for incident Type
def cr_text_preprocessing_for_incident_type(text):
    
    ## will replace the html characters with " "
    text =re.sub('<.*?>', ' ', text)
    
    #to remove the timestamp from description
    text=re.sub(r'\d{2}[-/]\d{2}[-/]\d{4} (2[0-3]|[01][0-9]|[0-9]):([0-5][0-9]|[0-9]):([0-5][0-9]|[0-9])',' ',text)
    
    ## remove the dash line and other characters
    text = re.sub('[^a-zA-Z0-9\.]',' ',text)   
    
    #will replace newline with space
    text = re.sub("\n"," ",text)
    
    #to remove the only digits
    text=re.sub(" \d+| \d+ ", " ", text)
    
    #will convert to lower case
    text = text.lower()
    
    # will split and join the words
    text=' '.join(text.split())  
    
    # removing the stop words
    text = ' '.join([word for word in text.split() if word not in (stopwords)])
    
    return text 


# CR Incident type prediction
def predict_cr_incident_type(Text_processed,Impact):
    
    #to convert str sentences into list
    input_data=[' '.join(Text_processed.split())]
    
    #loading the CR corpus used for incident modelling
    CR_incident_type_features_names = pickle.load(open(cr_incident_type_features_names_file, 'rb'))
        
    #converting the text data into vectors
    x=TfidfVectorizer(stop_words='english',vocabulary=CR_incident_type_features_names).fit_transform(input_data)
    
    #creating the features dataframe text vectors i.e.,x and add impact column 
    data=pd.DataFrame(data=x.toarray(),columns=CR_incident_type_features_names)
    data['Impact']=Impact
    data.replace(cr_impact_dict,inplace=True)
    
    
    #loading the model for predication
    cr_incident_model =  pickle.load(open(cr_incident_prediction_model_file, 'rb'))
    predicted_incident_type=cr_incident_model.predict(data)
    predicted_incident=''.join(predicted_incident_type)
    
    
    return predicted_incident    

# Pre-process for subgroup prediction
def cr_text_preprocessing_for_incident_subgrup(Text):
    
    #to remove the numbers from the text
    Text=re.sub(r'[0-9]',' ',Text)
    
    ### applying the lemmatization
    Text   = [' '.join([x.lemma_ for x in nlp(Text)])]
    
    return Text


# Predict CR incident Subgroup
def predict_cr_subgroup_incident_type(Text,Impact,predicted_incident_type):
    #loading the CR corpus used for incident modelling
    CR_subgroup_features_names = pickle.load(open(cr_subgroups_features_names_file, 'rb'))
      
        
    #converting the text data into vectors
    x=TfidfVectorizer(stop_words='english',vocabulary=CR_subgroup_features_names).fit_transform(Text)
       

    #creating the features dataframe text vectors i.e.,x and add impact column 
    data=pd.DataFrame(data=x.toarray(),columns=CR_subgroup_features_names)
    
    data['Impact']=Impact
    data['Incident']=predicted_incident_type
    # data.replace(['3 - Medium','2 - High','1 - Major'],[3,2,1],inplace=True)
    data.replace(cr_impact_dict,inplace=True)
    # data.replace(['Capacity Incidents','Network Incidents','Cloud Maintenance Incidents'],[1,2,3],inplace=True)
    data.replace(cr_incident_types_dict,inplace=True)
    cr_incident_types_dict
    list_of_incident_types=data.Incident.unique()
    
    
    ##building on decision tree model and saving the model with respective there groups

    for i in list_of_incident_types:
        data=data[data['Incident']==i]
        

        # subgroup prediction 
        if i == 1: #cacpcity
            subgroup_model = pickle.load(open(cr_capcity_subgroup_prediction_model, 'rb'))
            predicted_subgroup_number=subgroup_model.predict(data)
            Capacity_subgroup_list=['MKTM Service','USOSVC Issues','FHL Service','AWTM Service','Amex','MKHS Service','Token Issues','BMC Issues','Report Issues','Access Issues','TorchMark']
            predicted_subgroup_type=Capacity_subgroup_list[predicted_subgroup_number[0]]
            


        elif i == 2: # networks
            subgroup_model = pickle.load(open(cr_network_subgroup_prediction_model, 'rb'))
            predicted_subgroup_number=subgroup_model.predict(data)
            Network_subgroup_list=['FS Issues','FSM Issues','Nordstrom Issues','TorchMark','SRMS & CSU Issues','SM Issues']
            predicted_subgroup_type=Network_subgroup_list[predicted_subgroup_number[0]]
            

        elif i == 3: #Cloud
            subgroup_model = pickle.load(open(cr_cloud_subgroup_prediction_model, 'rb'))
            predicted_subgroup_number=subgroup_model.predict(data)
            Cloud_subgroup_list=['Azure maintenance','Amex']
            predicted_subgroup_type=Cloud_subgroup_list[predicted_subgroup_number[0]]
            
            
        else:
            predicted_subgroup_type = 'These are general accessing issues '  
            
            
    return predicted_subgroup_type        


# Function to return similar 
def cr_similar_incidents(predicted_incident_type,predicted_subgroup_incident_type):
    data=pd.read_csv(cr_dataset_file_path)
    data=data[['Description','Incidents','Subgroups']]
    similar_incidents=data[(data['Incidents']== predicted_incident_type) & (data['Subgroups']== predicted_subgroup_incident_type)]
    pd.options.display.max_colwidth = 120
    # similar_incident= similar_incidents['Description'].head(min(similar_incident_count,len(similar_incidents)))
    similar_incident= similar_incidents['Description'].tolist()
    # similar_incident.reset_index(drop=True,inplace=True)
    return similar_incident

# Function to display the potential problem on change request data
def cr_subgroup_component(predicted_incident_type,predicted_subgroup_incident_type,similar_incident):
    
    list_subgroup_having_component=['MKTM Service','USOSVC Issues','FHL Service','AWTM Service','Amex','MKHS Service']
    server_name_list = []
    if predicted_subgroup_incident_type  in list_subgroup_having_component :
        
        
    
        #to extract the alphanumberic value only
        for i in similar_incident:
            server_name=re.findall(r'\w+\d|\w+-\w+\d|fhl-\w+',i)[0]
            server_name_list.append(server_name)
    return server_name_list    
    
