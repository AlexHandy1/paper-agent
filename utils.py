import csv
import gspread
from google.oauth2.service_account import Credentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def save_articles_to_csv(articles, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Abstract', 'Published', 'Source'])
        for article in articles:
            title = article['Title']
            abstract = article['Abstract']
            published = article['Published']
            source = article['Source']
            writer.writerow([title, abstract, published, source])
    print(f"Saved {len(articles)} articles to {filename}")


def add_articles_to_gsheet(articles, gsheet_key, credentials_key_path, gsheet_tab_name):
    #setup connection - pre-requisite steps detailed here - # https://medium.com/@jb.ranchana/write-and-append-dataframes-to-google-sheets-in-python-f62479460cf0
    scopes = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']

    credentials = Credentials.from_service_account_file(credentials_key_path, scopes=scopes)

    gc = gspread.authorize(credentials)

    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)

    gs = gc.open_by_key(gsheet_key)
    article_values = [list(article.values()) for article in articles]
    gs.values_append(gsheet_tab_name, {'valueInputOption': 'RAW'}, {'values': article_values})

    print("Added ", len(articles), " articles to google sheet")

def get_worksheet_title_list(gsheet_key, credentials_key_path, gsheet_tab_name, tgt_col_num):
    #setup connection - pre-requisite steps detailed here - # https://medium.com/@jb.ranchana/write-and-append-dataframes-to-google-sheets-in-python-f62479460cf0
    scopes = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']

    credentials = Credentials.from_service_account_file(credentials_key_path, scopes=scopes)

    gc = gspread.authorize(credentials)

    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)

    gs = gc.open_by_key(gsheet_key)

    target_tab = gs.worksheet(gsheet_tab_name)
    tgt_list = target_tab.col_values(tgt_col_num)
    # print("Target values: ", tgt_list)
    return tgt_list

def parse_relevance_pred(raw_pred):
    if raw_pred == 1:
        return "Y"
    else:
        return "N"
