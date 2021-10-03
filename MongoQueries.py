import pymongo
import datetime

from pymongo.message import query
class QueryDB():

   def __init__(self) :
       #Prod--------------------------
       self.prodmyclient = pymongo.MongoClient("")
       self.prodmydb = self.prodmyclient['']
       self.prodmycol =self.prodmydb['']
       self.prodProductCol = self.prodmydb['']
       self.prodmyOrderCol = self.prodmydb['']
     
       #Date Formatting ----------------------------------------
       self.now = datetime.date.today()
       self.oneDayAhead =   self.now + datetime.timedelta(days=1)
       self.time_string = self.now.strftime("%m-%d-%Y")
       self.time_string2 = self.oneDayAhead.strftime("%m-%d-%Y")
       self.query =  { "$and": [{'orderCreatedDate': { "$gte" : '08-20-2021 00:00:00', "$lte": '08-21-2021 00:00:00' }}, { 'orderId': { "$exists": "true" } },{ 'orderLineItem.networkResource': { "$ne": [] } },{"$or":[{ 'orderStatusHistory.iotOrderStatus':"OrderActivationComplete"}, {'orderStatusHistory.iotOrderStatus':"OrderSubmitted"}]} ] } 
 
   def getDeviceCollectionFull(self, accountIds):
        deviceSimList = [items for items in self.prodmycol.find({'accountId': int(accountIds)})]
        
        return deviceSimList 
 
 
  #Using this function to return list of sims in device consolidation.     
   def getDeviceCollection(self, accountIds):
        print(accountIds)
        deviceSimList = []
        deviceSimList = [items['simNumber'] for items in self.prodmycol.find({'accountId': int(accountIds),'products': {'$exists' : False}, 'simNumber': {'$ne': '0000000000000000000000'}}, {'simNumber': 1, "_id":0})]
        return deviceSimList

   def getDeviceCollectionbySim(self, Sim):
        #print(Sim)
        deviceSimList = []
        deviceSimList = [items for items in self.prodmycol.find({'simNumber': str(Sim)})]
        return deviceSimList
       

   def getDeviceCollectionProducts(self, accountIds):
        #print(Sim)
        deviceSimList = []
        deviceSimList = [items for items in self.prodmycol.find({'accountId': int(accountIds)})]
        return deviceSimList    
  
   # Using this function to return the product info based on sim list  
   def getProductConfig(self, ratePlanName):
        query = {'$and': [{'$or':[{'shortDescription': ratePlanName}, {'ratePlan.ratePlanName': ratePlanName}]}, {'status': 'Published'}]}
        ratePlanInfo = self.prodProductCol.find(query)
        return list(ratePlanInfo)


   def getOrderCollection(self):
       orderList = []
       myDoc = self.prodmyOrderCol.find(self.query, {"_id": 0, "customerId": 1,"orderId": 1})
       for x in myDoc:
         orderList.append(x)
       return orderList

   def getOrderCollectionBySim(self):
       orderList = []
       myDoc = self.prodmyOrderCol.find(self.query, {"_id": 0, "customerId": 1,"orderId": 1})
       for x in myDoc:
         orderList.append(x)
       return orderList

   def getAccountsWithMissingRecurFreq(self):
       query =  [
    {
        '$match': {
             'products': {
                '$exists': True
            },
            'products.recurringFrequency': {
                '$exists': False
            }, 'simNumber': {'$ne': '0000000000000000000000'}
        }
    }, {
        '$group': {
            '_id': {
                'accountId': '$accountId'
            }
        }
    }
]   

       listOfAccount = self.prodmycol.aggregate(query)
       return list(listOfAccount)
   
   def insertMissingDevices(self, deviceList):
       self.prodmycol.insert_one(deviceList)
         

   def updateDeviceCollection(self, query, updateQuery):
        self.prodmycol.update_one(query, { "$set": updateQuery})  

   def updateArrayDeviceCollection(self, query, updateQuery, param):
        self.prodmycol.update_one(query, { '$set': updateQuery},upsert=True, array_filters=[{'products.productName' : { '$eq': str(param) }}])  

  

