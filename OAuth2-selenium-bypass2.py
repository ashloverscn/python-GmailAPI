import base64
import pandas as pd
from random import randint, choices
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from requests import HTTPError
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from jinja2 import Template
import ssl
import smtplib
import logging
import time as time
import sys
import pdfkit
import imgkit
import img2pdf
import os
import os.path
import string
from datetime import date
import uuid
import datetime
import threading

def run_authorization_flow():
    cred = flow.run_local_server(port=8080, open_browser=False)
    return cred

if __name__ == '__main__':

    CLIENT_SECRETS_FILE = "./credentials/ash.temp.new@gmail.com.json"
    SCOPES = ['https://mail.google.com/']
    flow = InstalledAppFlow.from_client_secrets_file("./credentials/ash.temp.new@gmail.com.json", SCOPES, redirect_uri='http://localhost:8080')
    auth_url, _ =  flow.authorization_url(prompt='consent')
    authorization_thread = threading.Thread(target=run_authorization_flow)
    authorization_thread.start()
    #driver = webdriver.Chrome()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    #driver = uc.Chrome()
    driver.maximize_window()
    driver.get(auth_url)
    print(auth_url)
    authorization_thread.join()

    
