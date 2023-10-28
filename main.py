from ProjectB_clientside_template_package.MainController import MainController
from ProjectB_clientside_template_package.ClientSocketControl.DataStructure import DataStructure
from ProjectB_clientside_template_package.Indicators.BollingerBands import BollingerBands
from datetime import datetime

class Main(MainController):
    def logicHandler(self, dataStructure:DataStructure):
        bollingerBands.addPrice(dataStructure.index)
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

m = Main()
m.login("funganything@gmail.com", "123");

bollingerBands = BollingerBands(20,2);

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

m.createDataStreamingRequest(dataStreamingRequest)
m.projectBTradeController(0.0005)
m.run()