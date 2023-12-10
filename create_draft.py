#https://github.com/googleworkspace/python-samples/blob/main/gmail/snippet/send%20mail/create_draft.py
import os.path
import base64
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

def gmail_create_draft():
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

    message.set_content("This is automated draft mail")

    message["To"] = "ash.temp.new@gmail.com"
    message["From"] = "ash.temp.new@gmail.com"
    message["Subject"] = "Automated draft"

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {"message": {"raw": encoded_message}}
    draft = (
        service.users()
        .drafts()
        .create(userId="me", body=create_message)
        .execute()
    )

    print(f'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')

  except HttpError as error:
    print(f"An error occurred: {error}")
    draft = None

  return draft


if __name__ == "__main__":
  gmail_create_draft()
