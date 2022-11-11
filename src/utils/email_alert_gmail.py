"""This function is used to send alert using gmail"""
import smtplib
import os
import ssl
import yaml


# Load config file
with open('config/config.yaml') as file:
  config= yaml.safe_load(file)
  #print(config)

#Get current working dir
cwd_path=os.getcwd()

# Different required paths
login_file=os.path.join(cwd_path,config['data_dir'],config['login_file'])

# function to read credentials
def read_creden():
    user=passw=''
    with open(login_file,'r') as f:
        file=f.readlines()
        user=file[0].strip()
        passw= file[1].strip()
    return user,passw       



def mail_gmail_send(receiver,predicted_incident,subgroup,resolution_time,incident_no):
    # define port
    port= 465

    #get the sender details
    sender,password= read_creden()
    incident_no=str(incident_no)

    
    subject='Resolution time'
    # body='it will take time to resolve the issuse around 2 hrs'
    body='''Hello, \n\n The following are details :\n \tIncident Number : {incident_no}\n \tPredicted Incident Category : {predicted_incident} \n \tPredicted Incident Sub-Category : {subgroup} \n \tExpected Resolution Time (in hr) : {resolution_time} \n\n\n Thanks,\n Support Team'''.format(incident_no=incident_no,predicted_incident=predicted_incident,subgroup=subgroup,resolution_time=resolution_time)

    message = f'Subject:{subject}\n\n{body}'

    context = ssl.create_default_context()

    #print('starting to send')

    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender, password) #login with mail_id and password
    # text = message.as_string()
    session.sendmail(sender, receiver, message)
    session.quit()
        
    #print('sent email')    