import pandas as pd
riskProfile = pd.read_excel('data/WM Manager Dashboard Data SetV2.xlsx', sheet_name='Risk Profile')

def getRiskProfile(client):
    risk = riskProfile[riskProfile["Client"] == client]
    return risk["Risk Profile"].iloc[0]

# print(getRiskProfile("CLIENT MONSIEUR"))