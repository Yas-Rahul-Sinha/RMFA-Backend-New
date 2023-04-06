import pandas as pd
from datetime import datetime

upcoming_meetings = pd.read_excel('data/WM Manager Dashboard Data SetV2.xlsx', sheet_name='Upcoming Meetings')

def checkMeetings(client):
    meetings = upcoming_meetings[upcoming_meetings["Client"] == client]
    if meetings.empty:
        return False
    else:
        return True

def getMeetingDate(client):
    meetings = upcoming_meetings[upcoming_meetings["Client"] == client]
    if checkMeetings(client):
        return str(meetings["Date"].iloc[0].strftime("%d %b %y"))
    else:
        return " "

def getMeetingTime(client):
    meetings = upcoming_meetings[upcoming_meetings["Client"] == client]
    if checkMeetings(client):
        return str(meetings["Time"].iloc[0].strftime("%I:%M %p"))
    else:
        return " "

# print(getMeetingDate("AUTO MAKER OSHAWA E"))
# print(getMeetingTime("AUTO MAKER OSHAWA E"))