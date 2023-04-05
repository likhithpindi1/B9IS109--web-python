import json

class JsonData:
    def __init__(self):
        self.getJsonFIle()
        
    def getJsonFIle(self):
        with open('keys.json', 'r') as fp:
            self.list_data = json.load(fp)
            fp.close()
            
    def getDjangoKey(self):
        return self.list_data['securityKey']
             
    def getFacebookData(self):
        return self.list_data['facebook']
    
    def getMailJet(self):
        return self.list_data['mailJet']
    
