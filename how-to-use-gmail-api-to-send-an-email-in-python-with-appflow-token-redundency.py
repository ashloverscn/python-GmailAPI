import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from requests import HTTPError
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase


emailId = 'ash.temp.new@gmail.com'
SCOPES = ['https://mail.google.com/']
creds = None

def gapisend(MIMEMultiMsg):
    if os.path.exists("./credentials/" + str(emailId) + "-token.json"):
       creds = Credentials.from_authorized_user_file("./credentials/" + str(emailId) + "-token.json", SCOPES)
    if not creds or not creds.valid:
       if creds and creds.expired and creds.refresh_token:
           creds.refresh(Request())
       else:
           flow = InstalledAppFlow.from_client_secrets_file(
               "./credentials/" + str(emailId) + ".json", SCOPES
               )
           creds = flow.run_local_server(port=0)
           auth_url, _ = flow.authorization_url(prompt='consent')

       with open("./credentials/" + str(emailId) + "-token.json", "w") as token:
              token.write(creds.to_json())
    service = build("gmail", "v1", credentials=creds)
    BASE64Msg = {'raw': base64.urlsafe_b64encode(MIMEMultiMsg.as_bytes()).decode()}
    try:
       SrvRsp = (service.users().messages().send(userId="me", body=BASE64Msg).execute())
       print(F'sent message to {SrvRsp} Message Id: {SrvRsp["id"]}')
    except HTTPError as error:
       print(F'An error occurred: {error}')
       SrvRsp = None

if __name__ == '__main__':
    emailMsg = 'You won $100,000'
    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = 'ashloverscn@gmail.com'
    mimeMessage['subject'] = 'You won'
    mimeMessage.attach(MIMEText(emailMsg, 'plain'))

    gapisend(mimeMessage)
    print('done')
