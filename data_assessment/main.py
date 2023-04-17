import math
import pandas as pd
from data_assessment.risk_profile import getRiskProfile
portfolios = pd.read_excel('data/WM Manager Dashboard Data SetV2.xlsx', sheet_name='Portfolio')
instrument_master_price = pd.read_excel('data/WM Manager Dashboard Data SetV2.xlsx', sheet_name='Instrument Master Price')
# portfolios = portfolios.transpose()
# for port in portfolios:
#     index = 0
#     for ins in master_price["Security_Description"]:
#         if(portfolios[port]["Security_Description"] == ins):
#             portfolios[port]["Market_Value"] = round(portfolios[port]["Units"]*master_price["Price-As of date"][index],2)
#             portfolios[port]["Market_Value_as_of_31st_Dec_2022"] = round(portfolios[port]["Units"]*master_price["Price 12/31/2022"][index],2)
#             portfolios[port]["Market_Value_as_of_30th_Sept_2022"] = round(portfolios[port]["Units"]*master_price["Price 09/30/2022"][index],2)
#             portfolios[port]["Market_Value_as_of_30th_June_2022"] = round(portfolios[port]["Units"]*master_price["Price 06/30/2022"][index],2)
#             portfolios[port]["Market_Value_as_of_31th_March_2022"] = round(portfolios[port]["Units"]*master_price["Price 03/31/2022"][index],2)
#             portfolios[port]["Market_Value_as_of_31th_Dec_2021"] = round(portfolios[port]["Units"]*master_price["Price 12/31/2021"][index],2)
#             portfolios[port]["Market_Value_as_of_31th_Dec_2020"] = round(portfolios[port]["Units"]*master_price["Price 12/31/2020"][index],2)
#             break
#         index+=1
#     if math.isnan(portfolios[port]["Market_Value"]):
#         portfolios[port]["Market_Value"] = 0
# portfolios = portfolios.transpose()
# # print(portfolios["Market Value"][5])
# # portfolio = pd.read_excel('WM Manager Dashboard Data SetV2.xlsx', sheet_name='Portfolio', usecols=[0, 1, 5, 11])
# temp = portfolios.Advisor[0]
# rows, columns = portfolios.shape
# # print(rows)
# # print(temp)
# temp2 = portfolios["Investor_Name"][0]
# bookSum = 0
# martSum = 0
# advisor = {}
# investor = []
# iterator = 0
# for ind in portfolios.Advisor:
#     if ind != temp or iterator == rows-1:
#         # print(ind != temp)
#         investor.append({"Investor":temp2,"Book_Value": round(bookSum,2), "MM": round(martSum,2), "Country_of_Domicile": portfolios["Account_Currency"][iterator], "Risk_Profile":getRiskProfile(temp2)})
#         temp2 = portfolios["Investor_Name"][iterator]
#         # print(temp2)
#         martSum = round(portfolios["Market_Value"][iterator],2)
#         bookSum = round(portfolios["Account_Investment_Book_Value"][iterator],2)
#         advisor.update({temp:investor.copy()})
#         # print(advisor)
#         temp = ind
#         # print(temp)
#         investor.clear()
#     elif ind == temp:
#         if temp2 != portfolios["Investor_Name"][iterator]:
#             # print(temp2)
#             investor.append({"Investor":temp2,"Book_Value": round(bookSum,2), "MM": round(martSum,2), "Country_of_Domicile": portfolios["Account_Currency"][iterator],"Risk_Profile":getRiskProfile(temp2)})
#             # print(temp2)
#             temp2 = portfolios["Investor_Name"][iterator]
#             # print(investor)
#             martSum = round(portfolios["Market_Value"][iterator],2)
#             bookSum = round(portfolios["Account_Investment_Book_Value"][iterator],2)
#         elif temp2 == portfolios["Investor_Name"][iterator]:
#             martSum += round(portfolios["Market_Value"][iterator],2)
#             bookSum += round(portfolios["Account_Investment_Book_Value"][iterator],2)
#             # print(bookSum)
#
#     iterator += 1
# # for i in advisor["Advisor 1"]:
# #     print(i)

def calculateBookValue(portfolio):
    for index,row in portfolio.iterrows():
        portfolio.at[index,"Account_Investment_Book_Value"] = round(row["Units"] * row["Unit_Price"],2)
    return portfolio
def getAllMarketValues(portfolio):
    portfolio = calculateBookValue(portfolio)
    for index,row in portfolio.iterrows():
        filter_row = instrument_master_price[instrument_master_price["Security_Description"] == row["Security_Description"]]
        if not filter_row.empty:
            portfolio.at[index,"Market_Value"] = round(filter_row.iloc[0]["Price-As of date"] * row["Units"],2)
            portfolio.at[index,"Market_Value_as_of_31st_Dec_2022"] = round(row["Units"] * filter_row.iloc[0]["Price 12/31/2022"], 2)
            portfolio.at[index,"Market_Value_as_of_30th_Sept_2022"] = round(row["Units"] * filter_row.iloc[0]["Price 09/30/2022"],2)
            portfolio.at[index,"Market_Value_as_of_30th_June_2022"] = round(row["Units"] * filter_row.iloc[0]["Price 06/30/2022"],2)
            portfolio.at[index,"Market_Value_as_of_31th_March_2022"] = round(row["Units"] * filter_row.iloc[0]["Price 03/31/2022"],2)
            portfolio.at[index,"Market_Value_as_of_31th_Dec_2021"] = round(row["Units"] * filter_row.iloc[0]["Price 12/31/2021"],2)
            portfolio.at[index,"Market_Value_as_of_31th_Dec_2020"] = round(row["Units"] * filter_row.iloc[0]["Price 12/31/2020"],2)
        else:
            portfolio.at[index, "Market_Value"] = 0
            portfolio.at[index, "Market_Value_as_of_31st_Dec_2022"] = 0
            portfolio.at[index, "Market_Value_as_of_30th_Sept_2022"] = 0
            portfolio.at[index, "Market_Value_as_of_30th_June_2022"] = 0
            portfolio.at[index, "Market_Value_as_of_31th_March_2022"] = 0
            portfolio.at[index, "Market_Value_as_of_31th_Dec_2021"] = 0
            portfolio.at[index, "Market_Value_as_of_31th_Dec_2020"] = 0
    return portfolio

def getClientList(advisor):
    portfolio = getAllMarketValues(portfolios)
    advisor_filter = portfolio[portfolio["Advisor"] == advisor]
    clients = advisor_filter["Investor_Name"].unique()
    temp1=[]
    temp2={}
    for client in clients:
        client_filter = advisor_filter[advisor_filter["Investor_Name"] == client]
        temp2["Book_Value"] = client_filter["Account_Investment_Book_Value"].sum()
        temp2["MM"] = client_filter["Market_Value"].sum()
        temp2["Investor"] = client
        temp2["Country_of_Domicile"] = "USD"
        temp2["Risk_Profile"] = getRiskProfile(client)
        temp1.append(temp2.copy())
    temp1.sort(key=lambda x:x["Book_Value"],reverse=True)
    return temp1

# print(getClientList("Gunasiri"))