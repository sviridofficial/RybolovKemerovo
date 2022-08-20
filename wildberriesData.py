import requests
from parserRibolov import get_info
from tokens import wildberriesApiKey
def getWildberriesData():
    url = "https://suppliers-api.wildberries.ru/api/v2/stocks?skip=0&take=10000"
    apiKey = wildberriesApiKey
    result = []
    ribolovUrl = "https://www.rybolov-kem.ru/component/virtuemart/product-details/"
    r = requests.get(url, headers={"Authorization": apiKey})
    data = r.json()
    for item in data["stocks"]:
        if len(item["article"])>3 and item["article"][:3]=="РВ-":
            if item["article"].count("РВ-")>1:
                doublicates = item["article"].split("РВ-")
                for doublicate in doublicates:
                    if len(doublicate)!=0:
                        result.append(ribolovUrl + doublicate[3:])
            else:
                result.append(ribolovUrl + item["article"][3:])

    return result



def getWildberriesDataForOstatki():
    url = "https://suppliers-api.wildberries.ru/api/v2/stocks?skip=0&take=10000"
    apiKey = wildberriesApiKey
    result = []
    ribolovUrl = "https://www.rybolov-kem.ru/component/virtuemart/product-details/"
    r = requests.get(url, headers={"Authorization": apiKey})
    data = r.json()
    for item in data["stocks"]:
        if len(item["article"])>3 and item["article"][:3]=="РВ-":
            if item["article"].count("РВ-")>1:
                doublicates = item["article"].split("РВ-")
                for doublicate in doublicates:
                    if len(doublicate)!=0:
                        result.append([ribolovUrl + doublicate[3:], item["barcode"]])
            else:
                result.append([ribolovUrl + item["article"][3:], item["barcode"]])

    return result

def getParsedDataForWildberries(data):
    index = 0
    result = []
    while index < len(data):
        try:
            index+=1
            print(str(index-1)+". "+data[index-1][0])
            result.append([get_info(data[index-1][0]), data[index-1][1]])

        except:
            print("Вылезла ошибка!")
            print("------------------------------------------")
            index = index-1
    return result

