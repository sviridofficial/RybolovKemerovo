import requests
from parserRibolov import Card
from removeDuplicate import getParsedData, removeDuplicate
from ozonData import getOzonData
from tokens import ozonApiKey, ozonClientId
def ozonOstatkiWork():
    clientId = ozonClientId
    apiKey = ozonApiKey
    getUrl = "https://api-seller.ozon.ru/v1/product/import/stocks"
    ozonData = getOzonData()
    ozonData = removeDuplicate(ozonData)
    parsedData = getParsedData(ozonData)
    countInRequest = 0 
    arrayForRequest = []
    for item in parsedData:
        new_instock = 0
        if int(item.get_instock())>50:
            new_instock = item.get_instock()
        elif int(item.get_instock())>25:
            new_instock = 10
        elif int(item.get_instock())>10:
            new_instock = 3
        else:
            new_instock = 0

        countInRequest +=1
        arrayForRequest.append({"offer_id": "РВ-"+item.get_articulInMarketPlace(), "stock": new_instock})
        if(countInRequest==100):
            r = requests.post(getUrl, headers={"Client-Id": clientId, "Api-Key": apiKey} , json={"stocks": arrayForRequest})
            print(r.status_code, len(arrayForRequest))
            arrayForRequest = []
            countInRequest = 0
        
    r = requests.post(getUrl, headers={"Client-Id": clientId, "Api-Key": apiKey} , json={"stocks": arrayForRequest})