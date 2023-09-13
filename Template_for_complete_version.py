import json

from ClientSocketControl.SocketClient import SocketClient
from ClientSocketControl.DataStructure import DataStructure
from Indicators.BollingerBands import BollingerBands
from TradeControl.OrderActionConstants.Action import Action
from TradeControl.TradeController import TradeController


#Login here
dataStreaming = SocketClient(/*email*/, /*password*/)

#Form JSON object message for data streaming request
dataStreamingRequest = {
    "activity":"@#activity#@",
    "market":"@#market#@",
    "index":"@#index#@",
    "startdate":"@#startdate#@",
    "enddate":"@#enddate#@",
    "starttime":"@#starttime#@",
    "endtime":"@#endtime#@",
    "interval":@#interval#@-1,
    "mitigateNoiseWithinPrecentage":@#mitigateNoiseWithinPrecentage#@
}

#Send the request to server
dataStreaming.request(dataStreamingRequest)

'''
This template included a simple account and order management function
You may modify the function to fit your back test
'''
tradeController = TradeController()
tradeController.setSlippage(@#slippage#@)

#Initial the ObjectMapper
mapper = json.JSONDecoder()
#Initial the JSONObject
response = None
    
#Setup the indicatories you need here
@#indicatories#@

while True:
    #get the response
    response = dataStreaming.getResponse()
    
    if response:
        #Convert response JSON message to Python dictionary
        dataStructure_dict = json.loads(response)
        dataStructure = DataStructure(**dataStructure_dict)
        
        #Check response finished or not
        if dataStructure.done:
            break
        
        #Check error caused or not
        if dataStructure.error:
            print(dataStructure.error)
            break
        
        #check the order allow to trade or not
        tradeController.tradeCheckingAndBalanceUpdate(dataStructure)
        
        '''
        You may write your back test program below within the while loop
        >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        '''
        @#indicatoriesUpdateLogic#@

        @#baseLogicResult#@
        
        @#logicGatewayResult#@
                                     
        @#actionAndTradeLogic#@
        
        '''
        <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        '''
        
        
