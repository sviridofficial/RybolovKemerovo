import requests
from wildberriesData import getWildberriesDataForOstatki, getParsedDataForWildberries
from removeDuplicate import removeDuplicate, getParsedData
from tokens import wildberriesApiKey
def wildberriesOstatki():
    apiKey = wildberriesApiKey
    updateOstatkiURL = "https://suppliers-api.wildberries.ru/api/v2/stocks"
    wildberriesData = getWildberriesDataForOstatki()
    parsedData = getParsedDataForWildberries(wildberriesData)
    countInRequest = 0 
    arrayForRequest = []
    for item in parsedData:
        new_instock = 0
        if int(item[0].get_instock())>50:
            new_instock = item[0].get_instock()
        elif int(item[0].get_instock())>25:
            new_instock = 10
        elif int(item[0].get_instock())>10:
            new_instock = 3
        else:
            new_instock = 0

        countInRequest +=1
        
        wirehouseId = 182223
        arrayForRequest.append({"barcode": item[1], "stock": int(new_instock), "warehouseId": int(wirehouseId)})
        if(countInRequest==1000):
            r = requests.post(updateOstatkiURL, headers={"Authorization": apiKey} , json=arrayForRequest)
            print(r.status_code, len(arrayForRequest))
            arrayForRequest = []
            countInRequest = 0
            print(r.json())

    r = requests.post(updateOstatkiURL, headers={"Authorization": apiKey} , json=arrayForRequest)
    
