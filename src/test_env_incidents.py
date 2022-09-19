'''This function is used to predict the resolution time'''

from utils.other_resolution_time import *
from utils.cr_prediction import *
from utils.env_predict import *
from utils.other_predict import *
from utils.pr_preprocessing import *
from utils.pr_change_type import *

description='''Change  AXEAN the  update rbestatus service (RBE) to update the services that has successfully scheduled the documents for process and has documents on the staging folder to in process. The service should update all the other documents to Error.'''
# description='''Change the signature for MB notification service to include the additional paramters to that we can ingest optional parameters of the notification message into our notification system. Please incorporate appropriate change in response to indicate if the optional parameters were included so that the users are aware of the request sent.'''

Impact='3 - Medium'


#initialize the value
is_change=False
is_env=False
is_other=False

is_change,is_env,is_other=env_or_change_type(description)
print(is_change,is_env,is_other)

# get the incident types
if is_change:
    predicted_incident_type,predicted_subgroup,similar_incident,similar_incident_count,server_name_list=cr_prediction(description,Impact)
elif is_env:
    predicted_incident_type,predicted_subgroup=env_predict(description)
elif is_other:
    predicted_incident_type,predicted_subgroup=other_predict(description,Impact)

print(predicted_incident_type,predicted_subgroup)

resolution_time=get_resolution_time(predicted_incident_type,predicted_subgroup,Impact)    
print(resolution_time) 
print(type(resolution_time))    
