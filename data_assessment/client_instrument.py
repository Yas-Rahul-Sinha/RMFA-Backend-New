from data_assessment.main import *
from utility.datautil import fetchMarketValuePercentage

portfolios = pd.read_excel('data/WM Manager Dashboard Data SetV2.xlsx', sheet_name='Portfolio')
portfolios = getAllMarketValues(portfolios)

def adv_investor_investment(advisor,client,account):
    filter_data = portfolios[portfolios["Account"] == account]
    temp = []
    temp2 = {}
    for index,row in filter_data.iterrows():
        temp2["Description"] = row["Security_Description"]
        temp2["Instrument_Type"] = row["Instrument_Type"]
        temp2["Units"] = row["Units"]
        temp2["Market_Value"] = row["Market_Value"]
        temp2["Book_Value"] = row["Account_Investment_Book_Value"]
        temp2["Portfolio_Weightage"] = fetchMarketValuePercentage(client,row["Security_Description"])
        temp2["Account"] = str(account)
        temp.append(temp2.copy())
    return temp

def getClientInstreumentData(advisor):
    filter_data = portfolios[portfolios["Advisor"] == advisor]
    clients = filter_data["Investor_Name"].unique()
    temp = {}
    temp2 = {}
    for client in clients:
        client_filter = filter_data[filter_data["Investor_Name"] == client]
        accounts = client_filter["Account"].unique()
        for account in accounts:
            temp2[str(account)] = adv_investor_investment(advisor,client,account)
        temp[client] = temp2.copy()
        temp2.clear()
    return temp

# print(getClientInstreumentData("Gunasiri"))

# adv_investor_investments = {}
# investor_investments = {}
# temp1 = []
# temp2 = {}
# temp3 = {}
# for adv in advisor:
#     for inv in advisor[adv]:
#         index = 0
#         for investor in portfolios["Investor_Name"]:
#             if inv["Investor"] == investor:
#                 temp2["Instrument_Type"] = portfolios["Instrument_Type"][index]
#                 temp2["Description"] = portfolios["Security_Description"][index]
#                 temp2["Units"] = portfolios["Units"][index]
#                 temp2["Market_Value"] = round(portfolios["Market_Value"][index],2)
#                 temp2["Book_Value"] = round(portfolios["Account_Investment_Book_Value"][index],2)
#                 temp2["Portfolio_Weightage"] = fetchMarketValuePercentage(inv["Investor"], portfolios["Security_Description"][index])
#                 temp2["Account"] = portfolios["Account"][index]
#                 if index == len(portfolios["Investor_Name"])-1:
#                     temp1.append(temp2.copy())
#                     temp3[temp2["Account"]] = temp1.copy()
#                     temp1.clear()
#                 elif temp2["Account"] != portfolios["Account"][index+1]:
#                     temp1.append(temp2.copy())
#                     temp3[temp2["Account"]] = temp1.copy()
#                     temp1.clear()
#                 else:
#                     temp1.append(temp2.copy())
#             index+=1
#         investor_investments[inv["Investor"]] = temp3.copy()
#         temp3.clear()
#     adv_investor_investments[adv] = investor_investments.copy()
#     investor_investments.clear()
# print(adv_investor_investments)
# for i in adv_investor_investments["Advisor 1"]:
#     print(i)


