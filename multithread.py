import threading
from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_SECRETS_FILE = "./credentials/ash.temp.new@gmail.com.json"
SCOPES = ['https://mail.google.com/']

flow = InstalledAppFlow.from_client_secrets_file("./credentials/ash.temp.new@gmail.com.json", SCOPES, redirect_uri='http://localhost:8080')
auth_url =  flow.authorization_url(prompt='consent')


def run_authorization_flow():
    authorization_url, _ = flow.run_local_server(port=8080, open_browser=False)
    #print(f'Please go to this URL to authorize: {authorization_url}')
    
authorization_thread = threading.Thread(target=run_authorization_flow)

authorization_thread.start()

for i in range(10):
    print(f"Main code running... {i}")
    auth_url =  flow.authorization_url(prompt='consent')
    print(auth_url)

authorization_thread.join()

print("Main code continues after authorization")
