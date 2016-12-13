import datetime

import httplib2
from apiclient import discovery
from .settings import SPREADSHEET_ID
from .auth import get_credentials


def get_service():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http('.cache'))
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    return discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)


def get_spreadsheet(service):
    rangeName = 'PocketMoney!A2:E'
    return service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID, range=rangeName,
        valueRenderOption='FORMATTED_VALUE'
    ).execute()


def add_transaction(description, in_amount, out_amount, service=None, spsheet=None):
    if service == None:
        service = get_service()
    if spsheet == None:
        spsheet = get_spreadsheet(service)
    new_cell_index = 2 + len(spsheet.get('values', []))  # range starts at A2

    date = datetime.datetime.today().strftime('%d-%b-%Y')
    description = description
    in_amount = in_amount
    out_amount = out_amount
    balance_formula = '=E{previous}+C{current}-D{current}'.format(
        previous=new_cell_index - 1, current=new_cell_index
    )
    body = {
        'values': [
            [date, description, in_amount, out_amount, balance_formula]
        ]
    }
    range = 'PocketMoney!A{}:E'.format(new_cell_index)

    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID, range=range,
        valueInputOption='USER_ENTERED', body=body
    ).execute()


def get_balance(service=None, spsheet=None):
    if service == None:
        service = get_service()
    if spsheet == None:
        spsheet = get_spreadsheet(service)

    values = spsheet.get('values', [])
    return values[-1][-1]
