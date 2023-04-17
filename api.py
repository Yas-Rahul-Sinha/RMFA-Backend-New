import ast
import importlib
import subprocess
import pythonanywhere_restarter

import dateutil
from flask_cors import CORS
from flask import Flask, request
from flask_restful import Resource,Api,reqparse

import data_assessment
import data_filter
from data_assessment.meeting_priority import *
from data_filter.filter_rule import *
from data_assessment.escalation import *
from data_assessment.main import *
from data_assessment.client_portfolio import getAccountPortfolio
from data_assessment.market_news import adv_market
# from data_assessment.client_instrument import *
from utility.datautil import *
from data_assessment.portfolio_level_accessment import *

app = app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


post_data = reqparse.RequestParser()
post_data.add_argument('Advisor',help='Advisor Name', required=True)
post_data.add_argument('Instrument',help='Instrument Name', required=True)
post_data.add_argument('Value',help='Value', required=True)

filter_data = reqparse.RequestParser()
filter_data.add_argument('Advisor',help="Advisor Name", required=True)
filter_data.add_argument('Rule1',help="Atleast one rule is required", required=True)
filter_data.add_argument('Rule2')

class ClientList(Resource):
    def get(self, adv):
        return {adv: getClientList(adv)}

class MarketNews(Resource):
    def get(self, adv):
        return {adv: adv_market[adv]}

class ClientEscalation(Resource):
    def get(self, adv):
        return {adv:getClientEscalations(adv)}

class CRM(Resource):
    def get(self, adv):
        # return {adv: temp3[adv]}
        rules = getRule(adv)
        ans = filter(rules)
        return {adv:ans}

class CRMDive(Resource):
    def get(self, cli):
        res = portfolioLevelAccessment(cli)
        return {cli:res}

class PortfolioData(Resource):
    def get(self,adv,client,account):
        return getAccountPortfolio(adv,client,account)

class MarketSignalImpact2(Resource):
    def post(self):
        response = {}
        temp = {}
        args = post_data.parse_args()
        for i in args["data"]:
            j = ast.literal_eval(i)
            temp["Existing_Value"] = fetchMarketValue(j["investor"], j["instrument"])
            temp["Projected_Value"] = calculateMarketValue(j["investor"], j["instrument"], j["value"])
            temp["Percentage_Impact"] = percentageImpact(temp["Existing_Value"], temp["Projected_Value"])
            if temp["Existing_Value"] > temp["Projected_Value"]:
                temp["Up/Down"] = "Down"
            elif temp["Existing_Value"] < temp["Projected_Value"]:
                temp["Up/Down"] = "Up"
            else:
                temp["Up/Down"] = "No Impact"
            response[j['instrument']] = temp.copy()
        return response

class MarketSignalImpact(Resource):
    def post(self):
        args = post_data.parse_args()
        return marketSignalImpact(args["Instrument"], args["Advisor"], args["Value"])

class ClientInstrumentData(Resource):
    def get(self,adv):
        return getClientInstreumentData(adv)

class AdvisorInstruments(Resource):
    def get(self, adv):
        return getAdvisorInstruments(adv)

class FundProjection(Resource):
    def get(self):
        return fundProjection()

class InstrumentData(Resource):
    def get(self):
        return getInstrumentData()

class FilterRule(Resource):
    def post(self):
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            json = request.json
            ans = filter(json)
            writeToSheet(json)
            importlib.reload(data_assessment)
            importlib.reload(data_filter)
            importlib.reload(dateutil)
            print(ans)
            return ans
        else:
            return 'Content-Type not supported!'

class EscalationCount(Resource):
    def get(self,adv):
        count = getEscalaionCount(adv)
        return count

class GetMeetingRules(Resource):
    def get(self,adv):
        rules = getRule(adv)
        return rules

# class ShutDown(Resource):
#     def get(self):
#         subprocess.run("shutdown -h 0", shell=True, check=True)
#         return "shutting down"

class Restart(Resource):
    # def get(self):
    #     subprocess.run("shutdown -r 0", shell=True, check=True)
    #     return "restarting"
    pythonanywhere_restarter.restartServer()


api.add_resource(ClientList, '/<string:adv>/clientList')
api.add_resource(MarketNews, '/<string:adv>/marketNews')
api.add_resource(ClientEscalation, '/<string:adv>/clientEscalation')
api.add_resource(CRM, '/<string:adv>/CRM')
api.add_resource(CRMDive, '/<string:cli>/CRMDive')
api.add_resource(PortfolioData, '/portfolioData/<string:adv>/<string:client>/<int:account>')
api.add_resource(MarketSignalImpact2, '/marketSignalImpact2')
api.add_resource(MarketSignalImpact, '/marketSignalImpact')
api.add_resource(ClientInstrumentData, '/clientInstrumentData/<string:adv>')
api.add_resource(AdvisorInstruments, '/advisorInstruments/<string:adv>')
api.add_resource(FundProjection, '/fundProjection')
api.add_resource(InstrumentData, '/instrumentData')
api.add_resource(FilterRule, '/filterRule')
api.add_resource(EscalationCount, '/<string:adv>/escalationCount')
api.add_resource(GetMeetingRules,'/<string:adv>/getMeetingRules')
# api.add_resource(ShutDown,'/shutdown')
api.add_resource(Restart,'/restart')
if __name__ == '__main__':
    app.run(debug=True)