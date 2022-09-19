""" This function is to predict the incident type, sibgroups related to other incidents"""

from utils.other_incident_type import *
from utils.other_incident_subgroup import *
from utils.other_preprocessing import *

def other_predict(description,Impact):
    
    # Pre-porcess data to get short, clean decription
    short_description,clean_short_description=data_preprocessing(description)

    # Predict incident type
    other_incident_type=get_other_incident_types(clean_short_description)
    #print(other_incident_type)

    # Additional pre-processing for subgroup
    processed_text=other_subgroup_preprocessing(clean_short_description)
    #print(processed_text)

    #Predict subgroups
    other_subgroup=predict_subgroup(processed_text,Impact,other_incident_type)
    #print(other_subgroup)
    return other_incident_type,other_subgroup