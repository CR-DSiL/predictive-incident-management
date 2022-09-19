from utils.pr_preprocessing import *
from utils.env_preprocessing import *
from utils.env_incident_predict import *
from utils.env_subgroup_predict import *
import string

"""This function predicts the incidents & Subgroups for env"""

def env_predict(description):
    
    #Pre-porcess data to get short, clean decription
    short_description,clean_short_description=data_preprocessing(description)

    # Env-pre-processing for incident Type
    pre_processed_text=env_preprocessing_for_incident_type(short_description)

    # env incident prediction
    predicted_incident_type=env_incident_predict(pre_processed_text)

    # env subgroup-proecessing
    pre_processed_text_subgroup=env_preprocessing_for_subgroups(short_description)

    #env sub group predict
    predicted_subgroup=env_subgroup_predict(pre_processed_text_subgroup)

    return predicted_incident_type.tolist(),predicted_subgroup.tolist()