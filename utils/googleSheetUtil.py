from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import time
import json
from google.oauth2.credentials import Credentials
import logging

logger = logging.getLogger(__name__)

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
#DEFAULT_SPREADSHEET_ID = "1_TbfksnMoBYot_C2Y0OLxolaJlhc-V-t7gt0j8RE3zk" # NBA

def readCell(sheet,spreadsheet_id,sheet_name,row_num,col_letter):
    '''
    sheet is the object
    '''
    # Should look like "Sheet1!A1:A1"
    a1_range = sheet_name+"!"+col_letter+str(row_num)+":"+col_letter+str(row_num)
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=a1_range).execute()
    cell_content = result.get('values', [])[0][0]
    return cell_content


def getNumRows(sheet,spreadsheet_id,sheet_name):
    column_to_check = sheet_name+"!A:A"
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=column_to_check).execute()
    values = result.get('values', [])
    num_rows = len(values)
    return num_rows


def connectToGoogleSheet(token_base_dir="utils"):
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    if token_base_dir is None:
        token_file = "token.json"
    else:
        token_filename = "token.json"
        token_file = os.path.join(token_base_dir,token_filename)
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    else:
        raise Exception("Can't find "+token_file+"!")

    # Call the Sheets API
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    return sheet


def writeFullRow(sheet,spreadsheet_id,sheet_name,row_num,row_content_list):
    '''
    sheet is the objext
    row_content_list is a list
    '''
    # Should look like "Sheet1!1:1"
    logger.debug("Waiting 1 second to be careful with Google limits...")
    time.sleep(1)
    a1_range = sheet_name+"!"+str(row_num)+":"+str(row_num)
    values = [row_content_list]
    body = {'values': values}
    value_input_option = "RAW"
    result = sheet.values().update(spreadsheetId=spreadsheet_id, valueInputOption=value_input_option,range=a1_range, body=body).execute()
    logger.debug('{0} cells updated.'.format(result.get('updatedCells')))

    return


def clearRowsRange(sheet,spreadsheet_id,sheet_name,row_num_a,row_num_b):
    # Should look like "Sheet1!1:1"
    logger.debug("Waiting 1 second to be careful with Google...")
    time.sleep(1)
    a1_range = sheet_name+"!"+str(row_num_a)+":"+str(row_num_b)
    body = {}
    logger.debug("About to clear: %s",a1_range)
    result = sheet.values().clear(spreadsheetId=spreadsheet_id, range=a1_range, body=body).execute()
    logger.debug("Completed the clear of: %s",result.get("clearedRange"))
    return


def A1ToGridRange(cell_a1,sheet_name,spreadsheet_id):
    # DANGEROUS HARDCODE!!!!!!
    # CHECK THIS METHOD
    # THE COLUMN WILL MAKE MISTAKES
    column = cell_a1[0]
    row = int(cell_a1[1:])
    sheet_id = getSheetID(spreadsheet_id,sheet_name)

    # Convert the column to an int
    num = ord(column.upper())-ord("A")

    col_a = num # 0 indexed
    col_b = num+1

    # row
    row_a = row-1
    row_b = row

    cell_gridrange = {
        "sheetId":sheet_id,
        "startRowIndex": row_a,
        "endRowIndex": row_b,
        "startColumnIndex": col_a,
        "endColumnIndex": col_b
    }

    print(cell_a1)
    print(cell_gridrange)
    return cell_gridrange


def findExistingRow(date,game_key,sheet,spreadsheet_id,sheet_name):
    row_num = None
    game_exists = False

    logger.debug("Hard coded pause for 1 second to be careful of Google limits")
    time.sleep(1)

    data_range = sheet_name+"!A:B"
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=data_range).execute()
    values = result.get('values', [])

    r = 1 # Because Google is 1 indexed
    for row in values:
        if date == row[0] and game_key == row[1]:
            row_num = r
            game_exists = True
            logger.debug("Found existing row #"+str(row_num)+" for game_key: "+game_key)
            break
        r += 1

    return row_num, game_exists

if __name__ == "__main__":
    # For debugging only
    spreadsheet_id = "1bh_On-6hfOOBdGcRgbH5QV2iUgQx3nOXTYkS7NkLVV0"
    sheet_id = "1815780437"
    sheet_name = "Regression Analysis"
    row_num = 2
    col_letter = "B"
    sheet = connectToGoogleSheet(token_base_dir=None)
    cell_content = readCell(
        sheet = sheet, 
        spreadsheet_id = spreadsheet_id, 
        sheet_name = sheet_name,
        row_num = row_num,
        col_letter = col_letter)
    print(cell_content)

    row_num = 8
    row_content_list = ["PZE","WM"]
    writeFullRow(
        sheet = sheet,
        spreadsheet_id = spreadsheet_id,
        sheet_name = sheet_name,
        row_num = row_num,
        row_content_list = row_content_list)
