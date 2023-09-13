import json

from ClientSocketControl.SocketClient import SocketClient
from ClientSocketControl.DataStructure import DataStructure
from Indicators.BollingerBands import BollingerBands
from TradeControl.OrderActionConstants.Action import Action
from TradeControl.TradeController import TradeController


#Login here
dataStreaming = SocketClient("funganything@gmail.com", "123")

#Form JSON object message for data streaming request
dataStreamingRequest = {
    "activity":"TickDataStreaming",
    "market":"Future",
    "index":"HSI",
    "startdate":"20230101",
    "enddate":"20230531",
    "starttime":"000000",
    "endtime":"235959",
    "interval":59,
    "mitigateNoiseWithinPrecentage":200
}

#Send the request to server
dataStreaming.request(dataStreamingRequest)

'''
This template included a simple account and order management function
You may modify the function to fit your back test
'''
tradeController = TradeController()
tradeController.setSlippage(0.0005)

bollingerBands = BollingerBands(20,2);

#Initial the ObjectMapper
mapper = json.JSONDecoder()
#Initial the JSONObject
response = None

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
        
        bollingerBands.addPrice(dataStructure.index);
        
        print(
            "{} {} {} {} {} {} {} {} {} {} {} {}".format(
                dataStructure.type,
                dataStructure.datetime,
                dataStructure.index,
                dataStructure.volumn,
                dataStructure.open,
                dataStructure.high,
                dataStructure.low,
                dataStructure.close,
                dataStructure.total_volumn,
                bollingerBands.getUpperBand(),
                bollingerBands.getMiddleBand(),
                bollingerBands.getLowerBand()
            )
        )
        
        #tradeController.placeOrder(dataStructure.symbol, Action.BUY.getAction(), 1)
        
        #print(tradeController.getProfile())
        
        '''
        <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        '''
        
        
