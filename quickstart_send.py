#https://developers.google.com/gmail/api/quickstart/python
import os.path
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

#SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
#SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
SCOPES = ['https://mail.google.com/']

def main():
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

  try:
    service = build("gmail", "v1", credentials=creds)
    
    emailMsg = 'You won $100,000'
    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = 'ash.temp.new@gmail.com'
    mimeMessage['subject'] = 'You won'
    mimeMessage.attach(MIMEText(emailMsg, 'plain'))
    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
    
    message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
    print(message)
    
  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()
