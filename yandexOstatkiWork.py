import requests
from yandexData import getYandexMarketData
from removeDuplicate import removeDuplicate,getParsedData
from tokens import yandexOauthToken, yandexClientId
def yandexOstatkiWork():
    url = "https://api.partner.market.yandex.ru/v2/campaigns/22578053/offers/stocks"
    clienId = yandexClientId
    oauthToken = yandexOauthToken
    yandexData = getYandexMarketData()
    yandexData = removeDuplicate(yandexData)
    parsedData = getParsedData(yandexData)

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
        arrayForRequest.append({
            "sku": "РВ-"+item.get_articulInMarketPlace(),
            "warehouseId": 149326,
            "items":
            [
            {
                "type": "FIT",
                "count": new_instock,
                "updatedAt": "2022-08-04T00:42:42+03:00"
            } 
            ]
        })
    r = requests.put(url, headers={'Authorization' : 'OAuth oauth_token='+oauthToken +', oauth_client_id =' + clienId, 'Accept': 'application/json'}, json={
        "skus": arrayForRequest
    })