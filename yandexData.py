import requests
from tokens import yandexClientId, yandexOauthToken
def getYandexMarketData():
    url = "https://api.partner.market.yandex.ru/v2/campaigns/22578053/offer-mapping-entries?limit=200"
    clienId = yandexClientId
    oauthToken = yandexOauthToken
    ribolovUrl = "https://www.rybolov-kem.ru/component/virtuemart/product-details/"
    r = requests.get(url, headers={'Authorization' : 'OAuth oauth_token='+oauthToken +', oauth_client_id =' + clienId, 'Accept': 'application/json'})
    data = r.json()
    result = []
    nextPageTokenExist =  len(data["result"]["paging"])>0
    for item in data["result"]["offerMappingEntries"]:
        if len(item["offer"]["shopSku"])>3 and item["offer"]["shopSku"][:3]=="РВ-":
                    result.append(ribolovUrl + item["offer"]["shopSku"][3:])
    if(nextPageTokenExist):
        while True:
            r = requests.get(url+"&page_token="+data["result"]["paging"]["nextPageToken"], headers={'Authorization' : 'OAuth oauth_token='+oauthToken +', oauth_client_id =' + clienId, 'Accept': 'application/json'})
            data = r.json()
            for item in data["result"]["offerMappingEntries"]:
                if len(item["offer"]["shopSku"])>3 and item["offer"]["shopSku"][:3]=="РВ-":
                    result.append(ribolovUrl + item["offer"]["shopSku"][3:])
            nextPageTokenExist =  len(data["result"]["paging"])>0
            if nextPageTokenExist==False:
                break
    return result           