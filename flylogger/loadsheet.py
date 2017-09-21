from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import pandas as pd

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
class GApp():
    def __init__(self, myid):
        self.scopes = 'https://www.googleapis.com/auth/spreadsheets'
        self.jsonfile = os.path.join('.', 'credentials', 'client_id.json')
        self.app_name = 'Google Sheets API Python Quickstart'
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        self.service = discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)
        self.spreadsheetId = myid

    def get_data(self, myrange):
        result = self.service.spreadsheets().values().get(
        spreadsheetId=self.spreadsheetId, range=myrange).execute()
        values = result.get('values', [])
        return values

    def find_credentials(self):
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        return os.path.join(credential_dir, 'sheets.googleapis.com-python.json')

    def get_credentials(self):
        credential_path = self.find_credentials()
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid: ### load credentials
            flow = client.flow_from_clientsecrets(self.jsonfile, self.scopes)
            flow.user_agent = self.app_name
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def import_stocks(self):
        gsheets = GApp('13Ry8lG1Uqq5Pq2jtOm0InvUGbn1ZNSmjfuovxxMoqJU')
        rangeName = 'All vials!A1:R77'
        values = gsheets.get_data(rangeName)
        header = values[0]
        df = {}
        for col in header:
            df[col] = []
        for row in values[1:]:
            if len(row) > 0:
                for key, val in zip(header, row):
                    df[key].append(val)
        df = pd.DataFrame(df)
        print("I found the following columns in your spreadsheet:")
        for each in df.columns:
            print(each)
        print(df.iloc[0])
