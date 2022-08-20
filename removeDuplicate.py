import numpy as np
from wildberriesData import getWildberriesData
from yandexData import getYandexMarketData
from ozonData import getOzonData
from parserRibolov import get_info
def removeDuplicate(list):
    data = np.array(list)
    return np.unique(data)

def getParsedData(data):
    index = 0
    result = []
    while index < len(data):
        try:
            index+=1
            if data[index-1].startswith("https://www.rybolov-kem.ru/component/virtuemart/product-details/"):
                print(str(index-1)+". "+data[index-1])
                result.append(get_info(data[index-1]))

        except:
            print("Вылезла ошибка!")
            print("------------------------------------------")
            index = index-1
    return result
