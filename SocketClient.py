import requests
import json
import threading
import socket


class SocketClient:    
    clientID = ""
    apiAccessCode = ""
    serverIPaddress = ""
    serverPort = ""
    JSONrequest = ""
    JSONresponse = []
    
    def __init__(self, loginname, password):
        self.loginname = loginname
        self.password = password
        obj = {
            "clientID": loginname,
            "password": password
        }
        result_in_String = requests.post("https://www.projectb.click/ProjectB/APIgetAccessCode.php", json = obj)
        result_in_JSON = json.loads(result_in_String.text)
        if(result_in_JSON["type"] is not None and result_in_JSON["type"]=="error"):
            raise Exception(result_in_JSON["message"])
        else:
            self.clientID = result_in_JSON["clientID"]
            self.apiAccessCode = result_in_JSON["accessCode"]
            
    def request(self, serverIPaddress, serverPort, requestObj):
        if(self.clientID is None or self.apiAccessCode is None):
            print("No available API access code")
        else:
            self.serverIPaddress = serverIPaddress
            self.serverPort = serverPort
            requestObj.update({"clientID": self.clientID})
            requestObj.update({"accessCode": self.apiAccessCode})
            self.JSONrequest = ""
            if(type(requestObj) is dict):
                self.JSONrequest = json.dumps(requestObj)
            t = threading.Thread(target = self.run)
            t.start()
            t.join()
    
    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.serverIPaddress, int(self.serverPort))
        sock.connect(server_address)
        
        #send request
        sock.send(self.JSONrequest.encode())

        #get response
        tempMessageFromServer = ""
        while True:
            messageFromServer = sock.recv(1)
            messageFromServer = messageFromServer.decode()
            if(messageFromServer is not None):
                if(messageFromServer != "\n"):
                    tempMessageFromServer += messageFromServer
                else:
                    if(tempMessageFromServer is not None):
                        if("done" in str(tempMessageFromServer)):
                            self.JSONresponse.append(None)
                            break
                        self.JSONresponse.append(tempMessageFromServer)
                        tempMessageFromServer = ""
                
    def getResponse(self):
        if(len(self.JSONresponse)>0):
            temp_JSONresponse = self.JSONresponse[0]
            self.JSONresponse.pop(0)
            return temp_JSONresponse
        else:
            return ""

