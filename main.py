print("Created by Francesco Massafra e Simone Ruggieri")



#Import all needed libraries
import httplib2
from googleapiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client import tools

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


FLOW = OAuth2WebServerFlow(                                                                                            
    client_id="YOUR CLIENT_ID",
    client_secret="YOUR CLIENT_SECRET",
    scope="https://www.googleapis.com/auth/contacts.readonly",
    user_agent="WHATEVER YOU WANT."
)
my_email="YOUR_EMAIL"                                                                                         #Login in GoogleSMTPServer using TLS protocol
password = "YOUR_PASSORD"
server = smtplib.SMTP('smtp.gmail.com',port=587)
server.starttls()
server.login(my_email, password)

storage = Storage("info.dat")                                                                                           #Saving or reading APIs credentials
credentials = storage.get()
if credentials is None or credentials.invalid == True:
    credentials = tools.run_flow(FLOW,storage)

http = httplib2.Http()                                                                                                  #Login and authorization to use the APIs
http = credentials.authorize(http)
people_service = build(serviceName='people',version="v1", http=http)
connections = people_service.people().connections().list(resourceName="people/me", personFields="names,emailAddresses") #Request to APIs for the informations

for x in connections.execute()["connections"]:
    print("invio email a :{}".format(x["emailAddresses"][0]["value"]))
    emailvalue = x["emailAddresses"][0]["value"]
    msg = MIMEMultipart()
    messaggio = "Email sent using Python to: {}".format(emailvalue)
    msg['From'] = my_email
    msg['To'] = emailvalue
    msg['Subject'] = "Email test python"
    msg.attach(MIMEText(messaggio, 'plain'))
    server.sendmail(msg['From'], msg['To'], msg.as_string())                                                            #Email sending...
server.quit()                                                                                                           #Exit from Google SMTP Server
