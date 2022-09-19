import imp
import pandas as pd
import numpy as np
import yaml
import os

# Load config file
with open('config/config.yaml') as file:
  config= yaml.safe_load(file)
  #print(config)

#Get current working dir
cwd_path=os.getcwd()

# Different required paths
resolution_time_lookup_file=os.path.join(cwd_path,config['models_dir'],config['resolution_time_lookup_file'])


def get_resolution_time(incident_type,predicted_subgroup_type,impact):
    Resolution_time_df=pd.read_csv(resolution_time_lookup_file)

    mean_time_df = Resolution_time_df[(Resolution_time_df['Incident_types']==incident_type) & (Resolution_time_df['Subgroups']==predicted_subgroup_type) & (Resolution_time_df['Impacts']==impact)]

    if mean_time_df.Average_Resolution_Time_Hour.empty:
        resolution_time='Data Not available'
    else:    
        resolution_time= mean_time_df['Average_Resolution_Time_Hour'].iloc[0]
        if np.isnan(resolution_time):
            resolution_time='Data Not available'
        else:          
            resolution_time=round(resolution_time,2)

    #change 
    resolution_time= mean_time_df['Average_Resolution_Time_Hour'].iloc[0]
    if np.isnan(resolution_time):
         resolution_time='Data Not available'
    else:          
        resolution_time=round(resolution_time,2)

    
    return resolution_time   