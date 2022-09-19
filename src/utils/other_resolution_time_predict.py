'''This function is used to predict the resolution time'''

from utils.other_resolution_time import *
from utils.cr_prediction import *
from utils.env_predict import *
from utils.other_predict import *
from utils.pr_preprocessing import *
from utils.pr_change_type import *

def incident_resolution_time(description,Impact):

    #initialize the value
    is_change=False
    is_env=False
    is_other=False

    is_change,is_env,is_other=env_or_change_type(description)
    #print(is_change,is_env,is_other)

    # get the incident types
    if is_change:
        predicted_incident_type,predicted_subgroup,similar_incident,similar_incident_count,server_name_list=cr_prediction(description,Impact)
    elif is_env:
        predicted_incident_type,predicted_subgroup=env_predict(description)
    elif is_other:
        predicted_incident_type,predicted_subgroup=other_predict(description,Impact)


    resolution_time=get_resolution_time(predicted_incident_type,predicted_subgroup,Impact)    
    
    return predicted_incident_type,predicted_subgroup,resolution_time