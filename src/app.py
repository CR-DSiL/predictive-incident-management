from os import abort
from flask import Flask, request,jsonify,Response
from utils.cr_prediction import *
from utils.env_predict import *
from utils.other_resolution_time_predict import *
from utils.email_alert_gmail import *



# Load config file
with open('config/config.yaml') as file:
  config= yaml.safe_load(file)
  #print(config)

#Get current working dir
cwd_path=os.getcwd()

# receiver email
receiver_email=config['receiver_email']


app = Flask(__name__)

@app.route('/')
def home():
    return 'Predcitve Incident Management'


@app.route('/change_request', methods=['POST'])
def change_request():
    # Data from postman
    description=str(request.args.get('description'))
    Impact=str(request.args.get('Impact'))

    #get the CR related predictions
    cr_predicted_incident,cr_subgroup,similar_incident,similar_incident_count,server_name_list=cr_prediction(description,Impact)

    return jsonify({'predicted_incident': cr_predicted_incident,'subgroup':cr_subgroup,'similar_incident':similar_incident,'similar_incident_count':similar_incident_count,'server_name_list':server_name_list})



@app.route('/env_change', methods=['POST'])
def env_change():
    # Data from postman
    description=str(request.args.get('description'))
    Impact=str(request.args.get('Impact'))

    #get the env related predictions
    predicted_incident_type,predicted_subgroup=env_predict(description)

    return jsonify({'predicted_incident': predicted_incident_type,'subgroup':predicted_subgroup})


@app.route('/service_request', methods=['POST'])
def service_request():
    # Data from postman
    description=str(request.args.get('description'))
    Impact=str(request.args.get('Impact'))

    #get the Service request related predictions
    predicted_incident_type,predicted_subgroup,resolution_time=incident_resolution_time(description,Impact)

    # send email alert
    mail_gmail_send(receiver_email,predicted_incident_type,predicted_subgroup,resolution_time)

    return jsonify({'predicted_incident': predicted_incident_type,'subgroup':predicted_subgroup,'resolution_time':resolution_time})


@app.route('/azure_webhook', methods=['POST'])
def azure_webhook():
     if request.method =='POST':
        
        #get the data
        data=request.json

        #get impact & Description
        impact_data=str(data['resource']['fields']['Microsoft.VSTS.Common.Priority']) 
        description =str(data['resource']['fields']['System.Description'])

        #convert impact data to required format
        Impact_dict={'1':'1 - Major','2':'2 - High','3':'3 - Medium','4':'3 - Low'}
        Impact=Impact_dict[impact_data]   
        print(Impact)
        print(description)

        #get the Service request related predictions
        predicted_incident_type,predicted_subgroup,resolution_time=incident_resolution_time(description,Impact)

        # send email alert
        mail_gmail_send(receiver_email,predicted_incident_type,predicted_subgroup,resolution_time)

        return Response(status=200)



    # # if request.method == 'POST':
    # #print("Data received from Webhook is: ", request.json)
    # description=str(request.json['message']['text'])
    # # Impact=str(request.json['resource']['fields']['Microsoft.Azure DevOps Services.Common.Severity'])
    # Impact=str(request.json['resource']['fields']['Microsoft.VSTS.Common.Priority'])
    # Impact_dict={'1':'1 - Major','2':'2 - High','3':'3 - Medium','4':'3 - Low'}
    # Impact=Impact_dict[Impact]

    # #get the Service request related predictions
    # predicted_incident_type,predicted_subgroup,resolution_time=incident_resolution_time(description,Impact)

    # # send email alert
    # mail_gmail_send(receiver_email,predicted_incident_type,predicted_subgroup,resolution_time)

    # return Response(status=200)
    # #return "Webhook received!", 200
    
    # else :
    #     abort(400)

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0',port=int(8080), debug=True)
    except:
         print("unexcepted error")
    
