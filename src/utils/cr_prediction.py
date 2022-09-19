from utils.cr_processing_util import *

'''This function 
@input : 
    Description : text
    Impact : Categorical
@Output :
    cr_predicted_incident:text
    cr_subgroup: text
    similar_incident: list
    server_name_list: list    
'''

def cr_prediction(description,Impact):
    #Text pre-processing for incident Type
    text_processed=cr_text_preprocessing_for_incident_type(description)
    # print(text_processed)

    # CR Incident type prediction
    cr_predicted_incident=predict_cr_incident_type(text_processed,Impact)
    #print(cr_predicted_incident)

    # Pre-process for subgroup prediction
    description_processed= cr_text_preprocessing_for_incident_subgrup(text_processed)

    # CR incident subgroup prediction
    cr_subgroup= predict_cr_subgroup_incident_type(description_processed,Impact,cr_predicted_incident)
    #print(cr_subgroup)

    # Similar incidents
    similar_incident=cr_similar_incidents(cr_predicted_incident,cr_subgroup)
    # print(similar_incident)

    # Number of similar incidents occured in past
    similar_incident_count=len(similar_incident)

    # Get components 
    server_name_list=cr_subgroup_component(cr_predicted_incident,cr_subgroup,similar_incident)
    #print(server_name_list)

    return cr_predicted_incident,cr_subgroup,similar_incident,similar_incident_count,server_name_list