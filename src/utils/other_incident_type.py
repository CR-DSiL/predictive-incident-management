"""
This function helps to get incident types for discriptions which are not related to evironment or change request related

input : description
Output : Incident Types
"""
import re

def get_other_incident_types (description):
    # Find Capcity Incident or Service Request Incident
    ispresent=re.findall('_wmi|wmi|Wmi|_Wmi|esx|mssql|- CRITICAL|- WARNING',description,flags=re.IGNORECASE)
    if ispresent:
        incident_type='Capacity Incident'
    else:
        incident_type='Service Request Incidents'    

    return incident_type