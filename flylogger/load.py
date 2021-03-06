from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import pandas as pd

from flylogger import cli, stock, yamlio

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
        self.app_name = 'Google Sheets Interface'
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        self.service = discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)
        self.spreadsheetId = myid
        sheet_metadata = self.service.spreadsheets().get(spreadsheetId=myid).execute()
        sheets = sheet_metadata.get('sheets', '')[0]
        self.name = sheets['properties']['title']
        self.allrange = "{}!A1:ZZ".format(self.name)
        self.owner = sheets['properties']['title']

    def get_data(self, myrange):
        if len(myrange) == 0:
            thisrange = self.allrange
        else:
            thisrange = myrange
        result = self.service.spreadsheets().values().get(
        spreadsheetId=self.spreadsheetId, range=thisrange).execute()
        values = result.get('values', [])
        return values

    def find_credentials(self):
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.flylogger')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        return os.path.join(credential_dir, 'credentials.json')

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

def find_key():
    home_dir = os.path.expanduser('~')
    print(home_dir)
    credential_dir = os.path.join(home_dir, '.flylogger')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    return os.path.join(credential_dir, 'keymapping.yaml')

def find_stocks():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.flylogger')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    return os.path.join(credential_dir, 'stocks.yaml')

def list_to_df(values):
    header = values[0]
    df = {}
    for col in header:
        df[col] = []
    for row in values[1:]:
        if len(row) > 0:
            for key, val in zip(header, row):
                df[key].append(val)
    return pd.DataFrame(df)

def stocks(sheet=None, srange=None):
    if sheet is None:
        if os.path.exists(find_stocks()) and cli.query_yn("Found stocks file. Do you want to use it?", default='yes'):
            sheetid = yamlio.read_yaml(find_stocks())['id']
            sheetrange = yamlio.read_yaml(find_stocks())['range']
        else:
            sheetid = cli.query_val("Type Google Sheet identifier", "[Can be found in the url address of your sheet after /d/]")
            sheetrange = cli.query_val("Type sheet range to import", "[Press ENTER if you want to load all data]")
            if cli.query_yn("Do you want to save this sheet for future use?", default='yes'):
                yamlio.write_yaml(find_stocks(), {'id': sheetid, 'range': sheetrange})
    else:
        sheetid = sheet
        sheetrange = srange

    gsheets = GApp(sheetid)
    values = gsheets.get_data(sheetrange)
    df = list_to_df(values)

    ### DataFrame to stocks collection
    keymapping = {}
    cols = list(each.lower() for each in df.columns)
    for ix, each in enumerate(stock.attrs):
        if each in cols:
            if cli.query_yn("Is column '{}': {}?".format(each, stock.descr[ix][0]), default='yes'):
                key = list(df.columns.values)[cols==each]
        ##elif close_match(each, cols):
        else:
            print("Attribute '{}' not found in current spreadsheet.".format(each))
            key = cli.query_val("Type column name for attribute '{}'".format(each), help='[possibilities: {}]'.format(list(df.columns.values)))
        keymapping[each] = key
    if cli.query_yn("Do you want to save this keymapping for future use?", default='yes'):
        yamlio.write_yaml(find_key(), keymapping)

    stock_collection = stock.Collection()
    for each_stock in df.iterrows():
        print(each_stock)
