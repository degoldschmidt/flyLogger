import tkinter as tk
import gspread
import pandas as pd
import oauth2client
import webbrowser
from oauth2client.service_account import ServiceAccountCredentials
import oauth2client.file
from flylogger.app import FlyloggerApp
from googleapiclient.discovery import build
import httplib2
from httplib2 import Http
from googleapiclient.errors import HttpError
import logging

class NoUserIdException(Exception):
  """Error raised when no user ID could be retrieved."""

def get_user_info(credentials):
    """Send a request to the UserInfo API to retrieve the user's information.

    Args:
    credentials: oauth2client.client.OAuth2Credentials instance to authorize the
                 request.
    Returns:
    User information as a dict.
    """
    user_info_service = build(serviceName='oauth2', version='v2', http=credentials.authorize(httplib2.Http()))
    user_info = None
    try:
        user_info = user_info_service.userinfo().get().execute()
    except HttpError as e:
        logging.error('An error occurred: %s', e)
    if user_info and user_info.get('id'):
        return user_info
    else:
        raise NoUserIdException()

def get_credentials():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive',
             'https://www.googleapis.com/auth/gmail.readonly',
             'https://www.googleapis.com/auth/userinfo.email',
             'https://www.googleapis.com/auth/userinfo.profile',
]

    _file = "credentials/client_secret_flylogger.json"
    """Gets google api credentials, or generates new credentials
    if they don't exist or are invalid."""
    flow = oauth2client.client.flow_from_clientsecrets(
            _file, scope,
            redirect_uri='urn:ietf:wg:oauth:2.0:oob')

    storage = oauth2client.file.Storage('credentials.dat')
    credentials = storage.get()

    if not credentials or credentials.invalid:
        auth_uri = flow.step1_get_authorize_url()
        webbrowser.open(auth_uri)

        auth_code = input('Enter the auth code: ')
        credentials = flow.step2_exchange(auth_code)

        storage.put(credentials)

    return credentials

def main():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    _file = "credentials/CRLabComp-degoldschmidt.json"
    credentials = get_credentials()#ServiceAccountCredentials.from_json_keyfile_name(_file, scope)
    user = get_user_info(credentials)

    #assuming parent is the frame in which you want to place the table
    root = tk.Tk()
    app = FlyloggerApp(root, credentials)
