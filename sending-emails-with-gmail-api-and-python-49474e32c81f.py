#https://medium.com/lyfepedia/sending-emails-with-gmail-api-and-python-49474e32c81f
#https://gist.github.com/Findeton/9e53b0f5a0f41183252192b689a44979/raw/33a733c2ab462ba59a9d10da4274345146af2137/send-email-gmail-api.py
import base64
import os
from apiclient import errors
from httplib2 import Http
from email.message import EmailMessage

#import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

#SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
#SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
SCOPES = ['https://mail.google.com/']

EMAIL_FROM = 'ash.temp.new@gmail.com'
EMAIL_TO = 'ash.temp.new@gmail.com'
EMAIL_SUBJECT = 'Hello!'
EMAIL_CONTENT = 'Hello, this is a test'

def create_message(sender, to, subject, message_text):
    message = EmailMessage()
    message.set_content(message_text)
    message["To"] = to
    message["From"] = sender
    message["Subject"] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)

def account_login():
  #creds, _ = google.auth.default()
  creds = None
  if os.path.exists("./credentials/token.json"):
    creds = Credentials.from_authorized_user_file("./credentials/token.json", SCOPES)
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "./credentials/credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    with open("./credentials/token.json", "w") as token:
      token.write(creds.to_json())
  service = build("gmail", "v1", credentials=creds)
  return service

if __name__ == "__main__":
  service = account_login()
  message = create_message(EMAIL_FROM, EMAIL_TO, EMAIL_SUBJECT, EMAIL_CONTENT)
  sent = send_message(service,'me', message)

