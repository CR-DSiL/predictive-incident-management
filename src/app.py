from os import abort
import pyodbc
import datetime
import random
from flask import Flask, request,jsonify,Response,render_template
from utils.cr_prediction import *
from utils.env_predict import *
from utils.other_resolution_time_predict import *
from utils.email_alert_gmail import *
from utils.outlook_mail_alert import *


# Load config file
with open('config/config.yaml') as file:
  config= yaml.safe_load(file)
  

#Get current working dir
cwd_path=os.getcwd()

# receiver email
receiver_email=config['receiver_email']

# get the db config
db_config=config['db_config']

app = Flask(__name__)

@app.route('/pim/')
def home():
    return render_template('Predictive Incident Management.html')


@app.route('/pim/dashboard')
def dashboard():
    return render_template('dashboard.html')


''' function return change potential risk prediction when the change request are raised'''
@app.route('/pim/change_request', methods=['POST'])
def change_request():
    # Data from postman
    if request.method == 'POST':
        description  = str(request.form.get('description'))
        Impact= str(request.form.get('Impact'))
        unformat_date =  datetime.datetime.now()
        Date = unformat_date.strftime("%Y-%m-%d %H:%M:%S")

        #connecting the database 
        try:
            conn = pyodbc.connect(**db_config)
            cursor=conn.cursor()
        except pyodbc.Error as e:
            error = " " 
            return e

        # Inserting the form values to tbl_change_request
        cursor.execute("INSERT INTO tbl_change_request (Date,Description,Impact) VALUES(?,?,?)",
        (Date,description,Impact))     
        conn.commit()

        # fetch the latest data from the tbl_change_request
        data = pd.read_sql_query('''SELECT Top 1 Id,Description,Impact FROM tbl_change_request ORDER BY ID DESC''', conn)
        Id,description,Impact = data.values[0]
        
        #get the CR related predictions
        cr_predicted_incident,cr_subgroup,similar_incident,similar_incident_count,server_name_list=cr_prediction(description,Impact)

        #For pushing the values to database conserding only one random value of past incident
        
        Past_Similar_Incident = random.choice(similar_incident)

        list_subgroup_having_component=['MKTM Service','USOSVC Issues','FHL Service','AWTM Service','Amex','MKHS Service']
    
        if Past_Similar_Incident == 'Data Unavailable..':
            Previous_Component_Servers_Affected = 'Data Unavailable..'
        else:
            if cr_subgroup in list_subgroup_having_component:
                Previous_Component_Servers_Affected = re.findall(r'\w+\d|\w+-\w+\d|fhl-\w+',Past_Similar_Incident)[0]  
            else:
                Previous_Component_Servers_Affected = 'Data Unavailable..'

        # Inserting the cr predicted values to tbl_change_request_predictions
        cursor.execute("INSERT INTO tbl_change_request_predictions (CR_Incident_Id,Incident_Type,CR_Subgroups,Previous_Component_Servers_Affected,Past_Similar_Incident_Count,Past_Similar_Incident_Description) VALUES(?,?,?,?,?,?)",
        (Id,cr_predicted_incident,cr_subgroup,Previous_Component_Servers_Affected,similar_incident_count,Past_Similar_Incident))     
        conn.commit()
       
        output_data = [
                {
                    'predicted_incident_type': cr_predicted_incident,
                    'predicted_subgroup': cr_subgroup,
                    'similar_incident': similar_incident[-4:],
                    'similar_incident_count':similar_incident_count,
                    'server_name_list': server_name_list
                } 
            ]
    return render_template('crprediction.html', data=output_data)
  

''' function return environmental prediction when the chnage request are related to environment '''
@app.route('/pim/env_change', methods=['POST'])
def env_change():
    # Data from postman
    description=str(request.form.get('description'))
    Impact=str(request.form.get('Impact'))
    unformat_date =  datetime.datetime.now()
    Date = unformat_date.strftime("%Y-%m-%d %H:%M:%S")

    #connecting the database
    conn = pyodbc.connect(**db_config)
    cursor=conn.cursor()

    # Inserting the form values to tbl_environment_change
    cursor.execute("INSERT INTO tbl_environment_change (Date,Description,Impact) VALUES(?,?,?)",
    (Date,description,Impact))     
    conn.commit()

    # fetch the latest data from the tbl_environment_change
    data = pd.read_sql_query('''SELECT Top 1 Id,Description,Impact FROM tbl_environment_change ORDER BY ID DESC''', conn)
    Id,description,Impact = data.values[0]
   
    #get the env related predictions
    predicted_incident_type,predicted_subgroup=env_predict(description)


    # Inserting the Environmental predicted values to tbl_environment_change_predicitons
    cursor.execute("INSERT INTO tbl_environment_change_predictions (Env_Change_Id,Incident_Type,Env_Subgroups) VALUES(?,?,?)",
    (Id,predicted_incident_type,predicted_subgroup))     
    conn.commit()

    output_data = [
        {
            'predicted_incident_type': predicted_incident_type,
            'predicted_subgroup': predicted_subgroup
        }
    ]

    return render_template('envprediction.html',data=output_data)



''' function return the incident resolution prediction for incidents '''
@app.route('/pim/azure_webhook', methods=['POST'])
def azure_webhook():
     if request.method =='POST':
        
        #get the data
        data=request.json

        #get impact & Description
        impact_data=str(data['resource']['fields']['Microsoft.VSTS.Common.Priority'])
        description =str(data['resource']['fields']['System.Description'])
        Date = data['resource']['fields']['System.CreatedDate']
        #Incident_Number = data['resource']['id']
        Incident_Number = str(data['resource']['fields']['Custom.IssueID'])

        #Process decription
        description=description.replace('<div>','')
        description=description.replace('</div>','')


        #convert impact data to required format
        Impact_dict={'1':'1 - Major','2':'2 - High','3':'3 - Medium','4':'4 - Low'}
        Impact = str(Impact_dict[impact_data])
        print(Impact)
        print(type(Impact))   


        #connecting the database 
        conn = pyodbc.connect(**db_config)
        cursor=conn.cursor()

        # Inserting the raw incident  values to tbl_incidents
        cursor.execute("INSERT INTO tbl_incidents (Date,Incident_Number,Description,Impact) VALUES(?,?,?,?)",
        (Date,Incident_Number,description,Impact))     
        conn.commit()

        # fetch the latest data from the tbl_environment_change
        data = pd.read_sql_query('''SELECT Top 1 Id,Description,Impact FROM tbl_incidents ORDER BY ID DESC''', conn)
        Id,description,impact_data = data.values[0]

        
        #get the Service request related predictions
        predicted_incident_type,predicted_subgroup,is_change,is_env,is_other,resolution_time = incident_resolution_time(description,impact_data)

        
        # Inserting the Incident predicted values to tbl_incidents_predictions
        cursor.execute("INSERT INTO tbl_incidents_predictions (Incident_Id,Incident_Type,Subgroups,Is_Change_Request,Is_Environmental_Change,Is_Service_Request,Average_Resolution_Time) VALUES(?,?,?,?,?,?,?)",
        (Id,predicted_incident_type,predicted_subgroup,is_change,is_env,is_other,resolution_time))     
        conn.commit()

        if resolution_time == 0.0:
            resolution_time= 'Data Not available'
            
        else:
            resolution_time=resolution_time

        # send email alert
        mail_outlook_send(receiver_email,predicted_incident_type,predicted_subgroup,resolution_time,Incident_Number)
        
        return Response(status=200)



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=int(8080), debug=True)
