import imp
import pyodbc
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

# get the db config
db_config=config['db_config']

# Different required paths
resolution_time_lookup_file=os.path.join(cwd_path,config['models_dir'],config['resolution_time_lookup_file'])


def get_resolution_time(incident_type,predicted_subgroup_type,impact):
    
    #database connection
    conn = pyodbc.connect(**db_config)
    cursor=conn.cursor()

    # getting the data from tbl_resolution_time_lookup
    Resolution_time_df=pd.read_sql_query (''' SELECT * FROM tbl_resolution_time_lookup ; ''', conn)
    
    # fetching the average resloution time for required data 
    mean_time_df = Resolution_time_df[(Resolution_time_df['Incident_Type']==incident_type) & (Resolution_time_df['Components_Subgroups']==predicted_subgroup_type) & (Resolution_time_df['Impact']==impact)]
    resolution_time= mean_time_df['Resolution_Time'].values
    
    if resolution_time.size != 0:
      resolution_time = resolution_time[0]
      resolution_time=round(resolution_time,2)
    else:
      resolution_time=0.0

    return resolution_time   