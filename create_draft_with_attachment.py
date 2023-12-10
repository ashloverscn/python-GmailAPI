#https://github.com/googleworkspace/python-samples/blob/main/gmail/snippet/send%20mail/create_draft_with_attachment.py
import base64
import mimetypes
import os
from email.message import EmailMessage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
#import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

#SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
#SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
SCOPES = ['https://mail.google.com/']

def gmail_create_draft_with_attachment():
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

    mime_message = EmailMessage()
    
    mime_message["To"] = "ash.temp.new@gmail.com"
    mime_message["From"] = "ash.temp.new@gmail.com"
    mime_message["Subject"] = "sample with attachment"

    mime_message.set_content(
        "Hi, this is automated mail with attachment.Please do not reply."
    )

    attachment_filename = "./contents/image.jpg"
    type_subtype, _ = mimetypes.guess_type(attachment_filename)
    maintype, subtype = type_subtype.split("/")

    with open(attachment_filename, "rb") as fp:
      attachment_data = fp.read()
    mime_message.add_attachment(attachment_data, maintype, subtype)

    encoded_message = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()

    create_draft_request_body = {"message": {"raw": encoded_message}}
    draft = (
        service.users()
        .drafts()
        .create(userId="me", body=create_draft_request_body)
        .execute()
    )
    print(f'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')
  except HttpError as error:
    print(f"An error occurred: {error}")
    draft = None
  return draft


def build_file_part(file):
  content_type, encoding = mimetypes.guess_type(file)

  if content_type is None or encoding is not None:
    content_type = "application/octet-stream"
  main_type, sub_type = content_type.split("/", 1)
  if main_type == "text":
    with open(file, "rb"):
      msg = MIMEText("r", _subtype=sub_type)
  elif main_type == "image":
    with open(file, "rb"):
      msg = MIMEImage("r", _subtype=sub_type)
  elif main_type == "audio":
    with open(file, "rb"):
      msg = MIMEAudio("r", _subtype=sub_type)
  else:
    with open(file, "rb"):
      msg = MIMEBase(main_type, sub_type)
      msg.set_payload(file.read())
  filename = os.path.basename(file)
  msg.add_header("Content-Disposition", "attachment", filename=filename)
  return msg


if __name__ == "__main__":
  gmail_create_draft_with_attachment()
