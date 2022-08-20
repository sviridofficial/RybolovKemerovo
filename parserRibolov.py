import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import codecs
import csv
import re
class Card:

        def __init__(self):
            self.name = None
            self.nal = None
            self.price = None
            self.description = None
            self.articul = None
            self.brand = None
            self.izm = None
            self.instock = 0
            self.articulInMarketPlace = None

        def get_name(self):
            return self.name

        def get_nal(self):
            return self.nal   

        def get_instock(self):
            return self.instock

        def get_price(self):
            return self.price

        def get_description(self):
            return self.description

        def get_articul(self):
            return self.articul

        def get_brand(self):
            return self.brand

        def get_izm(self):
            return self.izm

        def get_articulInMarketPlace(self):
            return self.articulInMarketPlace

        def display_info(self):
            print(f"Name: {self.name}\n"
                  f"Nalichie: {self.nal}\n"
                  f"Price: {self.price}\n"
                  f"Desrciption: {self.description}\n"
                  f"Articul: {self.articul}\n"
                  f"Brand: {self.brand}\n"
                  f"Ed.izm: {self.izm}\n"
                  f"Total instock: {self.instock}")
def get_html(url):
    ua = UserAgent()
    response = requests.get(url, headers = {'user-agent': f'{ua.random}'}).text
    return response

def get_info(response):
    crd = Card()
    crd.articulInMarketPlace = response.split("https://www.rybolov-kem.ru/component/virtuemart/product-details/")[1]

    ua = UserAgent()
    response = requests.get(response, headers = {'user-agent': f'{ua.random}'}).text
    soup = BeautifulSoup(response, 'lxml')

    
    
    
    error = soup.find('div', class_ = 'block-heading').text.strip()


    #print(error)

    if error == 'manager[0]':

        try:
            name = soup.find('div', class_ = 'title-pl').text.strip()
        except:
            name = None
        crd.name = name

        try:
            nal = soup.find('div', class_ = 'instock').text.strip()
        except:
            nal = None
        crd.nal = nal

        try:
            price = soup.find('div', class_ = 'price-wrap').find('span', class_ = 'price').text.strip()
        except:
            price = None
        crd.price = price

        try:
            description = soup.find('div', class_ = 'desc-wrap').text.strip()
        except:
            description = None
        crd.description = description

        try:
            inst = soup.find('form', class_ ='add_cart_form').find('input', {'name': 'total_instock'})['value']
        except:
            inst = None
        crd.instock = inst

        means = soup.find('div', class_ = 'info-wrap').find_all('div', class_ = 'info')

        for i in means:
            label = i.find('span', class_ = 'label').text.strip()
            #print(label)
            try:
                value = i.find('span', class_ = 'value').text.strip()
            except:
                value = None
            #print(value)

            if label == 'Артикул:':
                crd.articul = value
            elif label == 'Бренд:':
                crd.brand = value
            elif  label == 'Ед.изм:':
                crd.izm = value

    else:
        crd.nal = 'Товар не в наличии'

    return crd



