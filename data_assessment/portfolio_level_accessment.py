from numerize import numerize

from data_assessment.portfolio_info import *
from data_assessment.impact_calculation import *
from data_assessment.client_portfolio import *
from data_assessment.meeting_priority import getRule
from data_assessment.client_instrument import *

market_research = pd.read_excel("data/WM Manager Dashboard Data SetV2.xlsx", sheet_name="Market Research")
market_news = pd.read_excel("data/WM Manager Dashboard Data SetV2.xlsx", sheet_name="Market News")
def byMarketResearchPortfolio(accounts,category,type):
    category_filter = market_research[market_research["Category"] == category]
    type_filter = category_filter[category_filter["Type"] == type]
    type_filter = type_filter["Security_Description"].tolist()
    temp2={}
    temp3={}
    temp=[]
    temp4 = []
    for account in accounts:
        impact2 = 0
        instruments = getAccountInstruments(account)
        for instrument in instruments:
            if instrument in type_filter:
                impact1 = impactOnPortfolio(account,instrument)
                impact2 += impact1
                temp2["Account"] = account
                temp2["Impact"] = impact1
                temp2["Portfolio_Size"] = numerize.numerize(getPortfolioMarketValue(account))
                temp2["Reason"] = f"Impact of {round(impact1)}% on account {account} due to change in instrument {instrument} affected by change in {type} "
                # temp4.append(temp2.copy())
                temp.append(temp2.copy())
        # if len(temp4)!=0:
        #     temp3[account] = temp4
        # if abs(impact2) > 0:
        #     temp3["Overall_Impact"] = impact2
        # if len(temp3) != 0:
        #     temp.append(temp3.copy())
    return temp

def byMarketNewsPortfolio(accounts,category,type):
    category_filter = market_news[market_news["Category"] == category]
    type_filter = category_filter[category_filter["Impacts"] == type]
    temp = []
    temp3 = {}
    temp2 = {}
    temp4 = []
    for acc in accounts:
        ins = getAccountInstruments(acc)
        for ch in type_filter["Description"]:
            if ch in ins:
                    temp2["Account"] = acc
                    temp2["Impact"] = type
                    temp2["Reason"] = f"{type} news on {category} affting {ch}"
                    temp2["Portfolio_Size"] = numerize.numerize(getPortfolioMarketValue(acc))
                    temp.append(temp2.copy())
        #             temp4.append(temp2.copy())
        # if len(temp4)!=0:
        #     temp3[acc] = temp4
        # if len(temp3) != 0:
        #     temp.append(temp3.copy())
    return temp

def byInvestmentReviewPortfolio(accounts, type):
    temp = []
    temp2 = {}
    temp3 = {}
    temp4 = []
    if type == 'Portfolio Performance Related':
        for acc in accounts:
            prev_value = getPortfolioMarketValueAtTime(acc, "Market_Value_as_of_30th_Sept_2022")
            current_value = getPortfolioMarketValueAtTime(acc, "Market_Value_as_of_31st_Dec_2022")
            result = ((current_value - prev_value) / prev_value) * 100
            result = round(result, 2)
            if result < 0.2:
                temp2["Account"] = acc
                temp2["Impact"] = result
                temp2["Reason"] = f"Poor Account({acc}) Performance of yield {result}%"
                temp2["Portfolio_Size"] = numerize.numerize(getPortfolioMarketValue(acc))
                temp.append(temp2.copy())
        #         temp4.append(temp2.copy())
        # if len(temp4) != 0:
        #     temp3[acc] = temp4
        # if len(temp3) != 0:
        #     temp.append(temp3.copy())
    return temp

def checkForOther(client,condition):
    temp = []
    temp2 = {}
    if condition["MainCategory"] == "Investment Review" and condition["SubCategory"] == "Periodic Portfolio Review":
        all_clients = pd.read_excel("data/WM Manager Dashboard Data SetV2.xlsx",sheet_name="Periodic Performance Review")
        all_clients = all_clients["Client"].tolist()
        if client in all_clients:
            temp.append("This Client is on your Periodic Performance Review List")
    if condition["MainCategory"] == "Investment Review" and condition["SubCategory"] == "Personal Events":
        all_clients = pd.read_excel("data/WM Manager Dashboard Data SetV2.xlsx", sheet_name="Personal Events")
        temp_client = all_clients[all_clients["Event_Type"] == "Investment Review"]
        temp_client = temp_client["Client_Name"].tolist()
        if client in temp_client:
            temp.append(f"Client has upcoming Personal Event: {all_clients.loc[all_clients['Client_Name'] == client,'Event']}")
    if condition["MainCategory"] == "Investment Review" and condition["SubCategory"] == "Portfolio Recommendation":
        products = pd.read_excel("data/WM Manager Dashboard Data SetV2.xlsx", sheet_name="New Products")
        current_investment = getClientTotalInvestment(client)
        filter_products = products[products["Probability_Customer_Portfolio_Amount"] <= current_investment]
        recommended_product_df = filter_products[
            filter_products["Min_Investment_Required"] == filter_products["Min_Investment_Required"].max()]
        recommended_product = recommended_product_df["Product_Name"].iloc[0]
        temp.apppend(f"Product Recommendations:{recommended_product}")
    if condition["MainCategory"] == "Investment Review" and condition["SubCategory"] == "Additional Investment":
        data = pd.read_excel("data/WM Manager Dashboard Data SetV2.xlsx", sheet_name="Client Requested Meetings")
        filter_data = data[data["Reason"] == "Additional Investment"]
        required_data = filter_data[filter_data["Advisor"] == advisor]
        required_data = required_data["Client"].tolist()
        if client in required_data:
            temp.append("Client wants to make Additional Investment")
    if condition["MainCategory"] == "Other Client Communication":
        data = pd.read_excel("data/WM Manager Dashboard Data SetV2.xlsx", sheet_name="Client Requested Meetings")
        filter_data = data[data["Reason"] == condition["SubCategory"]]
        required_data = filter_data[filter_data["Type"] == condition["MainCategory"]]
        required_data = required_data["Client"].tolist()
        if client in required_data:
            temp.append(f"Other Client Communication:{condition['SubCategory']}")
    temp2["Other_Reasons"] = temp
    if len(temp) != 0:
        return [temp2]
    else:
        return []

def portfolioLevelAccessment(client):
    advisor = getAdvisor(client)
    accounts = getAccounts(client)
    rules = getRule(advisor)
    otherDetails = {}
    response = []
    for rule in rules["Rule"]:
        for condition in rule["Condition"]:
            if condition["MainCategory"] == "Market Research":
                res = byMarketResearchPortfolio(accounts,condition["SubCategory"],condition["SpecificImpact"])
                # print(f"res1:{res}")
                if len(res) != 0:
                    response.extend(res)
            if condition["MainCategory"] == "Market News":
                res = byMarketNewsPortfolio(accounts,condition["SubCategory"],condition["SpecificImpact"])
                # print(f"res2:{res}")
                if len(res) != 0:
                    response.extend(res)
            if condition["MainCategory"] == "Investment Review":
                res = byInvestmentReviewPortfolio(accounts,condition["SubCategory"])
                # print(f"res3:{res}")
                if len(res) != 0:
                    response.extend(res)
            else:
                res = checkForOther(client,condition)
                # print(f"res4:{res}")
                if len(res) != 0:
                    response.extend(res)
    otherDetails["Client Name"] = client
    otherDetails["Advisor"] = advisor
    otherDetails["Total_Investment"] = numerize.numerize(getClientTotalInvestment(client))
    response.append(otherDetails)
    return response


print(portfolioLevelAccessment("AUTO MAKER OSHAWA M"))