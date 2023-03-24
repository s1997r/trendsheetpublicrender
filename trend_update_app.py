# A very simple Flask Hello World app for you to get started with...

from flask import Flask, jsonify
from flask import request
import pandas as pd
import tweepy
from datetime import datetime, timedelta
from tweepy.auth import OAuthHandler
from datetime import timezone
#google Sheet Authentication
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe

app = Flask(__name__)

@app.route('/',methods = ['GET','POST'])
def updatetrends():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('sheets-api-project.json',scope)
    client = gspread.authorize(creds)
    # Open the desired spreadsheet
    spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1rSzgHtvNEB17B0hoP65QiH15qOw_Cu_4vvyijWSkTCU/edit#gid=0')
    # Select the first worksheet
    name_worksheet = datetime.now(timezone.utc).time().strftime("%I %p")

    #worksheet = spreadsheet.get_worksheet("Sheet1")
    try:
        spreadsheet.del_worksheet(spreadsheet.worksheet(name_worksheet))
    except:
        pass

    #worksheet = spreadsheet.worksheet("Sheet1")
    spreadsheet.add_worksheet(title=name_worksheet,rows="15000", cols="5")

    worksheet = spreadsheet.worksheet(name_worksheet)
    #worksheet.clear()
    fields = ['location_name', 'trend_name', 'trend_url','tweet_volume', 'time']
    worksheet.update([fields])



    #Auth
    auth = tweepy.OAuthHandler("EggqzYglkD01lMjE9W9niqWIL","Zbmr1M3ATDPSlAZvsCv45RsucZ6DAdZ28h8c0az88PqetgG4Kq")
    auth.set_access_token("1457262610487730178-UiGYUvaWJKghkJmrFxCgWfvcZogRaP","2IGAld5c6I1cRC2vJzuLIYl2OLq3o5tzKGoPwdT0LADUB")
    api = tweepy.API(auth)

    woeids = [1,23424738, 23424740, 23424747, 23424748, 23424750, 23424753, 23424757, 23424765, 23424768, 23424775, 23424782, 23424787,
              23424796, 23424800, 23424801, 23424802, 23424803, 23424819, 23424824, 23424829, 23424833, 23424834, 23424846, 23424848,
              23424852, 23424853, 23424856, 23424860, 23424863, 23424868,23424870, 23424873, 23424874, 23424898, 23424900, 23424901,23424908, 
              23424909, 23424910, 23424916, 23424919, 23424922, 23424923, 23424924, 23424925, 23424930, 23424934, 23424935, 23424936, 23424938,
              23424942, 23424948, 23424950, 23424954, 23424957, 23424960,23424969, 23424975, 23424976, 23424977, 23424982, 23424984]

    # Get the trending topics for the United States



    for id in woeids:
        df = pd.DataFrame()
        trends = api.get_place_trends(id=id)
        for trend in trends[0]['trends']:
                location_name = trends[0]['locations'][0]['name']
                trend_name = trend['name']
                trend_url = trend['url']
                tweet_volume = trend['tweet_volume']
                time = datetime.now(timezone.utc).time().strftime("%I %p")
                row = {"location_name":location_name,"trend_name":trend_name,"trend_url":trend_url,"tweet_volume":tweet_volume,"time":time}
                df = df.append(row,ignore_index=True)
        worksheet.append_rows(df.values.tolist())
