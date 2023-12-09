import base64
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError
from jinja2 import Template

SCOPES = [
        "https://www.googleapis.com/auth/gmail.send"
    ]
flow = InstalledAppFlow.from_client_secrets_file('./credentials/credentials.json', SCOPES)
creds = flow.run_local_server(port=0)

service = build('gmail', 'v1', credentials=creds)

sender_email = "ash.temp.new@gmail.com"
recipient_email = "ash.temp.new@gmail.com"
subject = "Hello from Python"
body = 'This is an email sent from Python using an HTML template and the Gmail SMTP server.'
with open('./contents/template.html', 'r') as f:
    template = Template(f.read())
context = {
    'subject': subject,
    'body': body
}
html = template.render(context)
message = MIMEText(context['body'], 'html')
message['Subject'] = subject
message['From'] = sender_email
message['To'] = recipient_email

create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

try:
    message = (service.users().messages().send(userId="me", body=create_message).execute())
    print(F'sent message to {message} Message Id: {message["id"]}')
except HTTPError as error:
    print(F'An error occurred: {error}')
    message = None
