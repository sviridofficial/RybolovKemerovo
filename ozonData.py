from unittest import result
import requests
from tokens import ozonApiKey, ozonClientId
def getOzonData():
    url = "https://api-seller.ozon.ru/v2/product/list"
    clientId = ozonClientId
    apiKey = ozonApiKey
    ribolovUrl = "https://www.rybolov-kem.ru/component/virtuemart/product-details/"
    result = []
    r = requests.post(url, headers={"Client-Id": clientId, "Api-Key": apiKey})
    data = r.json()
    for item in data['result']['items']:
        if len(item['offer_id'])>3 and item['offer_id'][:3]=="РВ-":
            result.append(ribolovUrl + item['offer_id'][3:])
    while True:
        r = requests.post(url, headers={"Client-Id": clientId, "Api-Key": apiKey}, json={"last_id": data["result"]["last_id"]})
        data = r.json()
        for item in data['result']['items']:
            if len(item['offer_id'])>3 and item['offer_id'][:3]=="РВ-":
                result.append(ribolovUrl + item['offer_id'][3:])
        if len( data['result']['items'])!=1000:
            break
    return result
