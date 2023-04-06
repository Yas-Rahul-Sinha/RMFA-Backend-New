import ast
import json

import pandas as pd
df = pd.read_excel("data/WM Manager Dashboard Data SetV2.xlsx", sheet_name="Filter Rule")
def getRule(advisor):
    temp = {}
    temp["Advisor"] = advisor
    temp2 = []
    for adv,rule in zip(df["Advisor"],df["Rule"]):
        if adv == advisor:
            temp2.append(ast.literal_eval(rule))
    temp["Rule"] = temp2.copy()
    return temp

# print(getRule("Gunasiri"))

