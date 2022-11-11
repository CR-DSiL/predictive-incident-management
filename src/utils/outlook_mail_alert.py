import smtplib
import os
import ssl
import yaml
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



# Load config file
with open('config/config.yaml') as file:
  config= yaml.safe_load(file)



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


def mail_outlook_send(receiver,predicted_incident,subgroup,resolution_time,incident_no):

    # define port
    smtp_port = 587

    #get the sender details
    sender,password= read_creden()
    incident_no=str(incident_no)


    msg = MIMEMultipart()
    msg['Subject'] = 'Incident Report'
    msg['From'] = sender
    COMMASPACE = ', '
    msg['To'] = COMMASPACE.join([sender, receiver])
    msg.preamble = 'Incident Report'

    # Attach HTML body
    msg.attach(MIMEText(
        '''
        <html>
            <body>
            <p style='margin-top:0cm;margin-right:0cm;margin-bottom:8.0pt;margin-left:0cm;line-height:107%;font-size:15px;font-family:"Calibri",sans-serif;'><span style='font-family:"Avenir Next Medium",sans-serif;color:#ED7D31;'>Cr</span><span style='font-family:"Avenir Next Medium",sans-serif;color:#4472C4;'>it</span><span style='font-family:"Avenir Next Medium",sans-serif;color:#ED7D31;'>ical</span><span style='font-family:"Avenir Next Medium",sans-serif;color:#4472C4;'>River Inc.</span></p>
    <p style='margin-top:0cm;margin-right:0cm;margin-bottom:8.0pt;margin-left:0cm;line-height:107%;font-size:15px;font-family:"Calibri",sans-serif;'><span style='font-family:"Avenir Next Medium",sans-serif;color:#4472C4;'>Predictive Incident Management - Report</span></p>
    <p style='margin-top:0cm;margin-right:0cm;margin-bottom:8.0pt;margin-left:0cm;line-height:107%;font-size:15px;font-family:"Calibri",sans-serif;'><span style='font-size:12px;line-height:107%;font-family:"Avenir Next",sans-serif;'>Hi,</span></p>
    <p style='margin-top:0cm;margin-right:0cm;margin-bottom:8.0pt;margin-left:0cm;line-height:107%;font-size:15px;font-family:"Calibri",sans-serif;'><span style='font-size:12px;line-height:107%;font-family:"Avenir Next",sans-serif;'>The incident report for the incident ticket you requested is as follows:</span></p>
    <table style="border-collapse:collapse;border:none;">
        <tbody>
            <tr>
                <td style="width: 198.2pt;border: 1pt solid windowtext;padding: 0cm 5.4pt;height: 14.95pt;vertical-align: top;">
                    <p style='margin-top:0cm;margin-right:0cm;margin-bottom:0cm;margin-left:0cm;line-height:normal;font-size:15px;font-family:"Calibri",sans-serif;'><span style='font-size:12px;font-family:"Avenir Next",sans-serif;'>Incident Number</span></p>
                </td>
                <td style="width: 116.1pt;border-top: 1pt solid windowtext;border-right: 1pt solid windowtext;border-bottom: 1pt solid windowtext;border-image: initial;border-left: none;padding: 0cm 5.4pt;height: 14.95pt;vertical-align: top;">
                    <p style='margin-top:0cm;margin-right:0cm;margin-bottom:0cm;margin-left:0cm;line-height:normal;font-size:15px;font-family:"Calibri",sans-serif;'><span style='font-size:12px;font-family:"Avenir Next",sans-serif;'>{incident_no}</span></p>
                </td>
            </tr>
            <tr>
                <td style="width: 198.2pt;border-right: 1pt solid windowtext;border-bottom: 1pt solid windowtext;border-left: 1pt solid windowtext;border-image: initial;border-top: none;padding: 0cm 5.4pt;height: 13.15pt;vertical-align: top;">
                    <p style='margin-top:0cm;margin-right:0cm;margin-bottom:0cm;margin-left:0cm;line-height:normal;font-size:15px;font-family:"Calibri",sans-serif;'><span style='font-size:12px;font-family:"Avenir Next",sans-serif;'>Predicted Incident Type</span></p>
                </td>
                <td style="width: 116.1pt;border-top: none;border-left: none;border-bottom: 1pt solid windowtext;border-right: 1pt solid windowtext;padding: 0cm 5.4pt;height: 13.15pt;vertical-align: top;">
                    <p style='margin-top:0cm;margin-right:0cm;margin-bottom:0cm;margin-left:0cm;line-height:normal;font-size:15px;font-family:"Calibri",sans-serif;'><span style='font-size:12px;font-family:"Avenir Next",sans-serif;'>{predicted_incident}</span></p>
                </td>
            </tr>
            <tr>
                <td style="width: 198.2pt;border-right: 1pt solid windowtext;border-bottom: 1pt solid windowtext;border-left: 1pt solid windowtext;border-image: initial;border-top: none;padding: 0cm 5.4pt;height: 14pt;vertical-align: top;">
                    <p style='margin-top:0cm;margin-right:0cm;margin-bottom:0cm;margin-left:0cm;line-height:normal;font-size:15px;font-family:"Calibri",sans-serif;'><span style='font-size:12px;font-family:"Avenir Next",sans-serif;'>Predicted Incident Sub-category</span></p>
                </td>
                <td style="width: 116.1pt;border-top: none;border-left: none;border-bottom: 1pt solid windowtext;border-right: 1pt solid windowtext;padding: 0cm 5.4pt;height: 14pt;vertical-align: top;">
                    <p style='margin-top:0cm;margin-right:0cm;margin-bottom:0cm;margin-left:0cm;line-height:normal;font-size:15px;font-family:"Calibri",sans-serif;'><span style='font-size:12px;font-family:"Avenir Next",sans-serif;'>{subgroup}</span></p>
                </td>
            </tr>
            <tr>
                <td style="width: 198.2pt;border-right: 1pt solid windowtext;border-bottom: 1pt solid windowtext;border-left: 1pt solid windowtext;border-image: initial;border-top: none;padding: 0cm 5.4pt;height: 12.85pt;vertical-align: top;">
                    <p style='margin-top:0cm;margin-right:0cm;margin-bottom:0cm;margin-left:0cm;line-height:normal;font-size:15px;font-family:"Calibri",sans-serif;'><span style='font-size:12px;font-family:"Avenir Next",sans-serif;'>Expected Resolution Time (hours)</span></p>
                </td>
                <td style="width: 116.1pt;border-top: none;border-left: none;border-bottom: 1pt solid windowtext;border-right: 1pt solid windowtext;padding: 0cm 5.4pt;height: 12.85pt;vertical-align: top;">
                    <p style='margin-top:0cm;margin-right:0cm;margin-bottom:0cm;margin-left:0cm;line-height:normal;font-size:15px;font-family:"Calibri",sans-serif;'><span style='font-size:12px;font-family:"Avenir Next",sans-serif;'>{resolution_time}</span></p>
                </td>
            </tr>
        </tbody>
    </table>
    <p style='margin-top:0cm;margin-right:0cm;margin-bottom:8.0pt;margin-left:0cm;line-height:107%;font-size:15px;font-family:"Calibri",sans-serif;'><span style='font-size:12px;line-height:107%;font-family:"Avenir Next",sans-serif;'>&nbsp;</span></p>
    <p style='margin-top:0cm;margin-right:0cm;margin-bottom:8.0pt;margin-left:0cm;line-height:107%;font-size:15px;font-family:"Calibri",sans-serif;'><span style='font-size:12px;line-height:107%;font-family:"Avenir Next",sans-serif;'>Regards,</span></p>
    <p style='margin-top:0cm;margin-right:0cm;margin-bottom:8.0pt;margin-left:0cm;line-height:107%;font-size:15px;font-family:"Calibri",sans-serif;'>AI\ML &amp; DevSecOps Support Team</p>
    <p style='margin-top:0cm;margin-right:0cm;margin-bottom:8.0pt;margin-left:0cm;line-height:107%;font-size:15px;font-family:"Calibri",sans-serif;'><em><span style='font-size:10px;line-height:107%;font-family:"Avenir Next",sans-serif;color:black;'>This email was sent to you as a result of your incident report on predictive incident management.</span></em></p>
    <p style='margin-top:0cm;margin-right:0cm;margin-bottom:8.0pt;margin-left:0cm;line-height:107%;font-size:15px;font-family:"Calibri",sans-serif;'><em><span style='font-size:11px;line-height:107%;font-family:"Avenir Next",sans-serif;color:black;'>&copy;&nbsp;</span></em><em><span style='font-size:10px;line-height:107%;font-family:"Avenir Next",sans-serif;color:#ED7D31;'>Cr</span></em><em><span style='font-size:10px;line-height:107%;font-family:"Avenir Next",sans-serif;color:#4472C4;'>it</span></em><em><span style='font-size:10px;line-height:107%;font-family:"Avenir Next",sans-serif;color:#ED7D31;'>ical</span></em><em><span style='font-size:10px;line-height:107%;font-family:"Avenir Next",sans-serif;color:#4472C4;'>River Inc. 2022</span></em></p>
    </body>
            </html>
            '''.format(incident_no=incident_no,predicted_incident=predicted_incident,subgroup=subgroup,resolution_time=resolution_time),

            'html', 'utf-8'))


    context = ssl.create_default_context()

    #Create SMTP session for sending the mail              
    session = smtplib.SMTP("smtp.office365.com", 587) #use gmail with port
    session.ehlo()  # Can be omitted
    session.starttls(context=context)
    session.ehlo()  # Can be omitted
    session.login(sender, password)
    #session.sendmail(sender, [sender, receiver], msg.as_string())
    session.sendmail(sender, receiver, msg.as_string())
    session.quit()
   