import pandas as pd
def import_portfolios():
    ws = pd.read_excel('WM Manager Dashboard Data SetV2.xlsx', sheet_name='Portfolio')
    return ws
def import_personal_event():
    ws = pd.read_excel('WM Manager Dashboard Data SetV2.xlsx', sheet_name='Risk Profile')
    return ws