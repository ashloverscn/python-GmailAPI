#https://github.com/googleworkspace/python-samples/blob/main/gmail/snippet/send%20mail/send_message.py
import base64
import os
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

def gmail_send_message():
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

  try:
    service = build("gmail", "v1", credentials=creds)

    message = EmailMessage()

    message.set_content("This is an automated mail")

    message["To"] = "ash.temp.new@gmail.com"
    message["From"] = "ash.temp.new@gmail.com"
    message["Subject"] = "Automated mail"

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {"raw": encoded_message}
    send_message = (
        service.users()
        .messages()
        .send(userId="me", body=create_message)
        .execute()
    )
    print(f'Message Id: {send_message["id"]}')
  except HttpError as error:
    print(f"An error occurred: {error}")
    send_message = None
  return send_message


if __name__ == "__main__":
  gmail_send_message()
