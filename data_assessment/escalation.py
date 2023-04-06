import pandas as pd
from data_assessment.portfolio_info import getClientTotalInvestment
# from data_assessment.main import advisor
# df = pd.read_excel('data/WM Manager Dashboard Data SetV2.xlsx', sheet_name='Client Escalation', usecols=[0, 4, 9, 10, 11, 12])
# clientEsc = df.transpose()
# rows, columns = clientEsc.shape
# clientlist = []
# for inv in clientEsc:
#     if clientEsc[inv]['Reason'] == 'Person Event' or clientEsc[inv]['Reason'] == 'Requested by client':
#         clientlist.append(clientEsc[inv])
# clientlist.sort(key=lambda d: d['Scheduled_Date'])
# iterator = 0
# temp = []
# crm = []
# for inv in clientEsc:
#     if clientEsc[inv]['Type_of_Escalation'] == 'Severe' and clientEsc[inv]['Reason'] != 'Requested by client' and clientEsc[inv]['Reason'] != 'Person Event':
#         temp.append(clientEsc[inv])
# temp.sort(key=lambda d:d['Performance'])
# crm.extend(temp)
# # print(clientlist)
# temp.clear()
# for inv in clientEsc:
#         if clientEsc[inv]['Type_of_Escalation'] == 'Moderate' and clientEsc[inv]['Reason'] != 'Requested by client' and clientEsc[inv]['Reason'] != 'Person Event':
#             temp.append(clientEsc[inv])
# temp.sort(key=lambda d: d['Performance'])
# crm.extend(temp)
# temp.clear()
# temp2 = {}
# temp3 = {}
# for adv in advisor:
#     for advClients in advisor[adv]:
#         for client in clientlist:
#             if client['Investor_Name'] == advClients["Investor"]:
#                 temp4 = client.to_dict()
#                 if pd.isna(temp4['Description']):
#                     temp4['Description'] = "No Description Provided"
#                 temp4['Scheduled_Date'] = str(temp4['Scheduled_Date'])
#                 temp.append(temp4)
#     temp2[adv] = temp.copy()
#     temp.clear()
# for adv in advisor:
#     for advClients in advisor[adv]:
#         for client in crm:
#             if client['Investor_Name'] == advClients["Investor"]:
#                 temp4 = client.to_dict()
#                 if pd.isna(temp4['Description']):
#                     temp4['Description'] = "No Description Provided"
#                 temp4['Scheduled_Date'] = str(temp4['Scheduled_Date'])
#                 temp.append(temp4)
#     temp3[adv] = temp.copy()
#     temp.clear()
#
# # for i in temp3["Advisor 1 "]:
# #     print(i)
# print(temp2)
def getClientEscalations(advisor):
    temp = []
    temp2 = {}
    all_meeting = pd.read_excel('data/WM Manager Dashboard Data SetV2.xlsx', sheet_name='Client Requested Meetings')
    client_escalation = all_meeting[all_meeting["Type"] == "Client Escalation"]
    advisor_specific_client_escalation = client_escalation[client_escalation["Advisor"] == advisor]
    for client,reason in zip(advisor_specific_client_escalation["Client"],advisor_specific_client_escalation["Reason"]):
        temp2["Investor_Name"] = client
        temp2["Reason"] = reason
        temp2["Total_Investment"] = getClientTotalInvestment(client)
        temp.append(temp2.copy())
    return temp

def getEscalaionCount(advisor):
    all_meeting = pd.read_excel('data/WM Manager Dashboard Data SetV2.xlsx', sheet_name='Client Requested Meetings')
    client_escalation = all_meeting[all_meeting["Type"] == "Client Escalation"]
    advisor_specific_client_escalation = client_escalation[client_escalation["Advisor"] == advisor]
    return len(advisor_specific_client_escalation["Reason"])

# print(getClientEscalations("Gunasiri"))
# print(getEscalaionCount("Gunasiri"))