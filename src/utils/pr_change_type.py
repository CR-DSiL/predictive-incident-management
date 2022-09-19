"""
This function check if the description is of change request type or Environment change type

input : full description
output :is_change,is_env (Boolean value : Yes, No)
"""


def env_or_change_type(description):
    is_other=False

    # check if its change request
    is_change=change_request(description)

    # check if its change request
    is_env=env_change(description)

    if ((is_change==False) & (is_env==False)):
        is_other=True
        
    return is_change,is_env,is_other


############################# Helper functions ####################################

# return a function to extract the change request tickets

change_request_keyword=["update","change","enhancement","release","deployment","implement","permission"]

def change_request(text):
    
    # converting all description text into lower case
    lower_text=text.lower()
    
    # identify the change request keyword in text and assign the boolean value
    for keyword in change_request_keyword:
        if keyword in lower_text:
            return True
        else:
            return False


# return a function to extract the change request tickets
Env_change_keyword=["sql","server","integration","load balance","notification","db","database","webserver","website","share","connectivity"]

def env_change(text):
    
    # converting all description text into lower case
    lower_text=text.lower()
    
    # identify the env request keyword in text and assign the boolean value
    for keyword in Env_change_keyword:
        if keyword in lower_text:
            return True
        else:
            return False

            