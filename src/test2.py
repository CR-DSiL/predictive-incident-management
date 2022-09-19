from utils.cr_prediction import *
from utils.pr_preprocessing import *
from utils.pr_change_type import *
from utils.other_incident_type import *
from utils.env_predict import *

from utils.other_predict import *
# description='''configure the fhl-xa service i.e. Microsoft Edge Update Service to perform the windows update the patches only during automatically and update the service to latest version. '''
description='''Change  AXEAN the  update rbestatus service (RBE) to update the services that has successfully scheduled the documents for process and has documents on the staging folder to in process. The service should update all the other documents to Error.'''
# description='''Change the signature for MB notification service to include the additional paramters to that we can ingest optional parameters of the notification message into our notification system. Please incorporate appropriate change in response to indicate if the optional parameters were included so that the users are aware of the request sent.'''

Impact='3 - Medium'

# # CR Realated
# cr_predicted_incident,cr_subgroup,similar_incident,server_name_list=cr_prediction(description,Impact)
# print(cr_predicted_incident,cr_subgroup,similar_incident,server_name_list)
# print(len(server_name_list))


#------------------------------------------------------------------
# description = ''' Production SQL Latency Issues - Contact History MKTMPRQCSQL01 Assistance Needed

# User Name: Phillip Holmes
# Employee/Agent ID: 17995
# Email Address: PBHOLMES@world.com
# Contact Number: 469-609-2409
# New or Existing Issue: New
# Remote or Office-based user: MCK
# Is the issue for yourself or being raised on behalf of someone else? Self
# Hardware or Software issue: NA
# Server Name if it's a server issue: MKTMPRQCSQL01 '''

 # Pre-porcess data to get short, clean decription
# short_description,clean_short_description=data_preprocessing(description)

# Get change type
# Find change type (env or change or other)