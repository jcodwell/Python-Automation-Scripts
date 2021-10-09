
import multiprocessing
from http_request import QueryDb
from http_request import HttpRequests

class Product:
    def __init__(self):
        self.productObj = {}
    #Builds Rateplan Object    
    def getRatePlanInfo(self, accountIds):
        dbObject = QueryDb.QueryDB()
        simList = dbObject.getDeviceCollection(accountIds)
        jasperSimApi = HttpRequests.HttpRequests()
        p2 = multiprocessing.Pool(8)
        jasperApi = p2.map(jasperSimApi.getJasperSimInfo, simList)
        print("Finished Ratplans")
        jasperList = [(jasperApi[item]['accountId'], jasperApi[item]['iccid'] ,jasperApi[item]['ratePlan']) for item in range(0, len(jasperApi))] 
        p2.close()
        p2.join()
        return jasperList


    #Queries DB and And RateplanObj to Build productObj
    def buildProductObject(self, ratePlanObj):
       dbObject = QueryDb.QueryDB()
       query = dbObject.getDeviceCollectionbySim(ratePlanObj[1])    
       getOrderInfo = HttpRequests.HttpRequests()
       orderInfo = getOrderInfo.getOrderByOrderIdsbyCustomerId(ratePlanObj[1], ratePlanObj[0])
       productInfo = dbObject.getProductConfig(str(ratePlanObj[2]))
       accountId = ratePlanObj[0]
       if orderInfo == None:
           productObj = {}
       else:
        productObj = {
           'products' : [{ 
               "productOfferOrderId" : str(productInfo[0]['productId'])+ "-" + str(productInfo[0]['ratePlan']['ratePlanId']),
               "productId": productInfo[0]['productId'],
               "productName": productInfo[0]['shortDescription'],
               "productDescription":  productInfo[0]['shortDescription'],
               "productClassification" : productInfo[0]['productClassification'],
                "productType" : "RATEPLAN",
               
                "offer" : {
                "offerType" : "RATEPLAN",
                "version" : productInfo[0]['ratePlan']['version'],
                "offerId" : productInfo[0]['ratePlan']['ratePlanId'],
                "orderId" : orderInfo.setdefault("orderId", ""),
                "chargeAllocation" : productInfo[0]['ratePlan']['chargeAllocation'],
                "effectiveDate" : {
                    "date" : productInfo[0]['effectiveDate']
                  },
                
                "status": {
                "statusCode": "Active",    
                "reasonCode": "Activation",
                "modifiedDate": " "
                    } 
                },
                "chargeIngested" : "false",
                "chargeType" :  productInfo[0]['chargeType'] ,
                "recurringFrequency" : "MONTHLY",
                "productOfferPrice" :  productInfo[0]['productOfferPrice']
           }]
           }
        dbObject.updateDeviceCollection(query[0], productObj)
        print(query[0])
        with open(str(accountId) + ".txt", "a") as f:
            f.write("\n" + 'SimNumber: ' + str( ratePlanObj[1]) + "\n" + 'RatePlans: ' + str(ratePlanObj[2]) + "\n" +'Products: ' + str(productObj) )
            
        return productObj

    # Function Run for building product and rateplan Obj    
    def run(self, accountID):
        selfClassObj = Product()
        print("start")
        p1 = multiprocessing.Pool(8)
        productsList = p1.map(selfClassObj.buildProductObject, selfClassObj.getRatePlanInfo(accountID))
        print("Finished")
        p1.close()
        p1.join()  
        return print(productsList)    

if __name__ == "__main__":
    test = Product()
    test.run('accountId')
