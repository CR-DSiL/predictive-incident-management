import requests
import json

webhook_url='http://127.0.0.1:8080/azure_webhook'

data={
    'description':'''Change  AXEAN the  update rbestatus service (RBE) to update the services that has successfully scheduled the documents for process and has documents on the staging folder to in process. The service should update all the other documents to Error.''',
'Impact':'3 - Medium'
}

r=requests.post(webhook_url,data=json.dumps(data),headers={'Content-Type':'application/json'})