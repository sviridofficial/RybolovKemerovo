from msilib.schema import Error
import threading
from tkinter import *
from tkinter import font
import tkinter
from PIL import ImageTk, Image
import webbrowser
import customtkinter
from ozonData import getOzonData
from wildberriesData import getWildberriesData
from yandexData import getYandexMarketData
from removeDuplicate import removeDuplicate
from parserRibolov import Card, get_info
import csv
import os
from tkinter import filedialog
from ozonOstatkiWork import ozonOstatkiWork
from yandexOstatkiWork import yandexOstatkiWork
from wildberriesOstatkiWork import wildberriesOstatki

def browsefunc():
    filePath = filedialog.askopenfilename(filetypes=(("tiff files","*.csv"),("All files","*.*")))
    labelForFilePath.configure(text="Выбран файл: " + filePath)

def getParsedData(data):
    index = 0
    result = []
    errorCounter = 0
    while index < len(data):
        try:
            index+=1
            print(index)
            if data[index-1].startswith("https://www.rybolov-kem.ru/component/virtuemart/product-details/"):
                label.configure(text="Делаю парсинг данных... "+ str(index)+" из " +str(len(data)-1))
                result.append(get_info(data[index-1]))
                errorCounter = 0
        except:
            print("Вылезла ошибка!")
            print("------------------------------------------")
            errorCounter+=1
            if(errorCounter>10):
                raise Error
            index = index-1
    return result
def updateOstatki():
    threadUpdate = threading.Thread(target=updateOstatkiThread)
    threadUpdate.start()


def updateOstatkiThread():
    b1.configure(state = tkinter.DISABLED)
    b2.configure(state=tkinter.DISABLED)
    clearButton.configure(state=tkinter.DISABLED)
    b3.configure(state=tkinter.DISABLED, width=155, text="Выполняется")
    label.configure(text="Обновляю остатки на Вайлдберис... ")
    try:

        wildberriesOstatki()
        label.configure(text="Обновляю остатки на Озон... ")
        ozonOstatkiWork()
        label.configure(text="Обновляю остатки на Яндекс... ")
        yandexOstatkiWork()
        label.configure(text="Выполнение завершено... ")
    except:
        label.configure(text="Произошла ошибка... ")
    b2.configure(state=tkinter.NORMAL)
    b1.configure(state = tkinter.NORMAL)
    b3.configure(state=tkinter.NORMAL, width=155, text = "Обновить остатки на МП")
    

def run_action():
    b1.configure(state = tkinter.DISABLED, text= "Выполняется")
    b2.configure(state=tkinter.DISABLED)
    clearButton.configure(state=tkinter.DISABLED)
    b3.configure(state=tkinter.DISABLED, width=155)
    textbox.delete()
    try:
        data = getOzonData()+getWildberriesData()+ getYandexMarketData()
        data = removeDuplicate(data)
        text = ""
        for i in data:
            text += i+"\n"
        textbox.insert(tkinter.END, text)
    except:
        textbox.insert(tkinter.END, "Произошла ошибка...\nВозможные причины:\n1)Отсутствует интернет-соединение\n2)Частые запросы к маркетплейсам\n3)Технические проблемы на серверах маркетплейсов")

    b2.configure(state=tkinter.NORMAL)
    b1.configure(state = tkinter.NORMAL, text="Получить ссылки для парсинга")
    b3.configure(state=tkinter.NORMAL, width=155)
    clearButton.configure(state=tkinter.NORMAL)

def check_thread(thread, message, finishMessage):
        if thread.is_alive():
            window.after(100, lambda: check_thread(thread, message, finishMessage))
            label.configure(text=message)
        else:
            label.configure(text=finishMessage)

def getUrlsForParsing():
    thread = threading.Thread(target=run_action)
    thread.start()
    check_thread(thread, message="Получаю данные...", finishMessage="Получение ссылок завершено!")
    
def parseThread():
    b1.configure(state = tkinter.DISABLED)
    b2.configure(state=tkinter.DISABLED, text= "Выполняется")
    clearButton.configure(state=tkinter.DISABLED)
    b3.configure(state=tkinter.DISABLED, width=155)
    text = textbox.getText()
    list = text.split("\n")
    try:
        list = getParsedData(list)
        label.configure(text="Формирую Excel файл...")
        with open("parserData.csv", 'w', encoding='utf-8') as f:
            headers = ['Название товара', 'Наличие', 'Цена', 'Описание товара', 'Артикул сайт', 'Бренд', 'Единицы измерения', 'Остатки', 'Артикул на МП']
            writer = csv.writer(f)
            writer.writerow(headers)
            for item in list:
                writer.writerow([item.get_name(), item.get_nal(), item.get_price(), item.get_description(), item.get_articul(), item.get_brand(), item.get_izm(), item.get_instock(), item.get_articulInMarketPlace()])
            label.configure(text="Выполнение завершено...")
            os.startfile("parserData.csv")
    except:
        label.configure(text="Произошла ошибка...")
    b2.configure(state=tkinter.NORMAL, text="Спарсить данные")
    b1.configure(state = tkinter.NORMAL)
    b3.configure(state=tkinter.NORMAL, width=155)
    clearButton.configure(state=tkinter.NORMAL)
def parsingOnClick():
    text = textbox.getText()
    if text=="\n":
        label.configure(text="Список ссылок пуст!")
    else:
        thread = threading.Thread(target=parseThread)
        thread.start()
        #check_thread(thread, message="Делаю парсинг сайта...", finishMessage="Парсинг данных завершен!")

def clearButton():
    label.configure(text="")
    textbox.delete()

def change_appearance_mode():
        if customtkinter.get_appearance_mode()=='Dark':
            customtkinter.set_appearance_mode("Light")
        else:
            customtkinter.set_appearance_mode("Dark")
        
def btn_clicked():
    print("Button Clicked")

def callback():
    webbrowser.open_new("https://www.rybolov-kem.ru/")


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")
window = customtkinter.CTk() 
window.iconbitmap('icon.ico')
window.geometry("1000x600")
window.configure(bg = "#ffffff")
window.title("РЫБОЛОВ КЕМЕРОВО")
filePath = ""
canvas = Canvas(
    window, height=300, width=250
)
frame =  customtkinter.CTkFrame(master=window, corner_radius=0, border_width=2)
frame.place(relwidth=0.3, relheight=1)

img = ImageTk.PhotoImage(Image.open("logo.png"))
label = Label(frame, image=img)
label.place(rely=.4, relx=.05)
link1 = customtkinter.CTkButton(master=frame, text="Наш сайт", command=callback)
link1.place(rely= .7, relx=.25)
optionmenu_1 = customtkinter.CTkSwitch(master=frame, command=change_appearance_mode, text="Изменить тему")

optionmenu_1.place(rely= .9, relx=.25)
frame2 = customtkinter.CTkFrame(master=window, corner_radius=0)
frame2.place(relwidth=1, relheight=1, relx=.3)

b1 = customtkinter.CTkButton(master=frame2, text="Получить ссылки для парсинга", command=getUrlsForParsing, width=230)
b2 = customtkinter.CTkButton(master=frame2, text="Спарсить данные", command=parsingOnClick)
b3 = customtkinter.CTkButton(master=frame2, text="Обновить остатки на МП", command=updateOstatki)
clearButton = customtkinter.CTkButton(master=frame2, text="Очистить поле", fg_color=("#f44336","#ba000d"), hover_color="red", command=clearButton, width=155)
b1.place(rely= .1, relx=.05)
b2.place(rely= .1, relx=.32)
b3.place(rely= .1, relx=.5)
filepathButton = customtkinter.CTkButton(master=frame2, text="Выбрать Excel для остатков", command=browsefunc)
filepathButton.place(rely= .38, relx=.05)
clearButton.place(rely=.38, relx=.52)
label = customtkinter.CTkLabel(master = frame2,text="", text_font = (22))
label.place(rely= .2, relx=.25)

textbox = customtkinter.CTkTextbox(master = frame2, border_width=0, corner_radius=10, width=620, height=300)

textbox.grid(row=0, column=0, sticky="nsew")
labelForFilePath = customtkinter.CTkLabel(master = frame2,text="", text_font = ("",8))
labelForFilePath.place(rely= .30, relx=.05)
v = customtkinter.CTkScrollbar(master = frame2, command=textbox.yview)
v.place(rely = 0.47, relx=0.64)
textbox.configure(yscrollcommand=v.set)
textbox.place(rely= .45, relx=.05)
window.resizable(False, False)
window.mainloop()
