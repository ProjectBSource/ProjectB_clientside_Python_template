import json
import time
from SocketClient import SocketClient

sc = SocketClient("funganything@gmail.com", "123")
obj = {
    "activity":"DataStreaming",
    "market":"Future",
    "index":"YM",
    "startdate":"20210701",
    "enddate":"20210801",
    "starttime":"120000",
    "endtime":"130000",
    "interval":"59",
}

sc.request(obj)


def getDate(response):
    if "date" in response:
        return response["date"]
    else:
        return None
    
def getTime(response):
    if "time" in response:
        return response["time"]
    else:
        return None
    
def getDateTime(response):
    if "datetime" in response:
        return response["datetime"]
    else:
        return None
    
def getIndex(response):
    if "index" in response:
        return response["index"]
    else:
        return None
    
def getVolumn(response):
    if "volumn" in response:
        return response["volumn"]
    else:
        return None
    
def getOpen(response):
    if "open" in response:
        return response["open"]
    else:
        return None
    
def getHigh(response):
    if "high" in response:
        return response["high"]
    else:
        return None
    
def getDate(response):
    try:
        if "date" in response:
            return response["date"]
        else:
            return None
    except:
        print("response:")
    
def getLow(response):
    if "low" in response:
        return response["low"]
    else:
        return None
    
def getClose(response):
    if "close" in response:
        return response["close"]
    else:
        return None
    
def getTotalVolumn(response):
    if "total volumn" in response:
        return response["total volumn"]
    else:
        return None
    

while(True):
    response = sc.getResponse()
    if(response is None):
        break
    if(len(response)>0):
        response = json.loads(response)
        print(
            getDate(response),",",
            getTime(response),",",
            getDateTime(response),",",
            getIndex(response),",",
            getVolumn(response),",",
            getOpen(response),",",
            getHigh(response),",",
            getLow(response),",",
            getClose(response),",",
            getTotalVolumn(response)
        )

        
        