# sahur-system-[2] / v-1.0 / 19.07.2026 - analytics 

import os
import sys
import subprocess
import json
import webbrowser
import shutil
import socket
import requests
import time
import datetime
import tkinter
from pythonping import ping

public_ip = "none"
local_ip = "none"
datetime_now = "none"
valutes = {'eur':'none', 'usd':'none', 'cny':'none'}
disk_data = {'vsego':'none','zanyato':'none','svobodno':'none'}


def ip():
 # белый айпи
  global public_ip, local_ip
  try: public_ip = requests.get('https://ifconfig.me', timeout=5).text.strip()
  except requests.RequestException as e: public_ip = f"Ошибка при получении белого IP: {e}"
 # серый айпи
  try:
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
  except: local_ip = 'Ошибка при получении локального IP'
  if len(local_ip) <= 13: local_ip = local_ip+"  "
  if len(public_ip) <= 13: public_ip = public_ip+"  "


def disk():
    path = '/'
    usage = shutil.disk_usage(path) # получаем информацию о диске
    gb = 2 ** 30 # байты в гигабайты
    disk_data['vsego'] = f"Всего: {usage.total / gb:.2f} GB"
    disk_data['zanyato'] = f"Занято: {usage.used / gb:.2f} GB"
    disk_data['svobodno'] = f"Свободно: {usage.free / gb:.2f} GB"
def get_currency_rate():
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    response = requests.get(url)
    if response.status_code == 200:
            data = response.json()
        # Поиск курса валюты по её коду (например, USD или EUR)
            valutes['eur'] = data['Valute']["EUR"]['Value']
            valutes['usd'] = data['Valute']["USD"]['Value']
            valutes['cny'] = data['Valute']["CNY"]['Value']
            return "yea"
    else: return "Ошибка подключения к серверу"

def _ping():
    response = ping("8.8.8.8", count=4) # ICMP-запросы
    r = response.rtt_avg_ms
    if len(str(r)) <= 3: return str(r)+" "
    return r

# функция мониторинга интернет соеденения 
# мониторинг задержки
# мониторинг связи узлов
# мониторинг места на диске


def update_time():
    current_text = label.cget("text")
    new_text = str(datetime.datetime.now())[:-7]
    # Обновляем текст в метке
    label.config(text=new_text, width=18, height=1,font=("Arial", 9))
    label.place(x=210,y=10)

    r_ping = _ping()
    ping = tkinter.Label(root, text=f"ping : {r_ping}")    
    ping.place(x=250,y=95)

    # Планируем следующий вызов этой же функции через 1000 мс (1 секунду)
    root.after(1000, update_time)


def write():
    with open('output.txt', 'w') as file:
       file.write(entry.get())
def read():
  try:
    with open('output.txt', 'r') as file:
        r = tkinter.Label(root, text=file.read())
        r.place(x=180,y=120)
  except FileNotFoundError: print("файл не найден")


root = tkinter.Tk()
root.title("Sahur Analytics")
#root.iconbitmap(r"")
root.geometry("350x200")
root.wm_attributes('-alpha', 0.9)
root.configure(bg="#584e4e") # или root['bg'] = 'blue'

label = tkinter.Label(root, font=("Arial", 9))
label.place(x=180,y=10)

root.after(1000, update_time)


ip = ip()
label_local_ip = tkinter.Label(root, text="L IP: "+local_ip)
label_local_ip.place(x=232, y=40)
label_public_ip = tkinter.Label(root, text="P IP: "+public_ip)
label_public_ip.place(x=231, y=65)

valutes_s = get_currency_rate()
eur_ = tkinter.Label(root,text=f"EUR : {valutes['eur']}", width=12, height=1,font=("Arial", 9))    
eur_.place(x=250, y=125)
usd_ = tkinter.Label(root,text=f"USD : {valutes['usd']}", width=12, height=1,font=("Arial", 9))
usd_.place(x=250, y=148)
cny_ = tkinter.Label(root,text=f"CNY : {valutes['cny']}", width=12, height=1,font=("Arial", 9))
cny_.place(x=250, y=171)

_disk = disk()
name_d = tkinter.Label(root, text=" Диск ")
name_d.place(x=125, y=100)
vse = tkinter.Label(root, text=disk_data['vsego'])
vse.place(x=125, y=125)
zan = tkinter.Label(root, text=disk_data['zanyato'])
zan.place(x=125, y=148)
svo = tkinter.Label(root, text=disk_data['svobodno'])
svo.place(x=125, y=171)



bt_1 = tkinter.Button(root, text='Чтение', command=read)
bt_1.place(x=10, y=40)
bt_1 = tkinter.Button(root, text='Выйти', command=root.destroy)
bt_1.place(x=10, y=10)


entry = tkinter.Entry(root, width=15)
entry.place(x=10, y=145)
button = tkinter.Button(root, text="запись",width=12, command=write)
button.place(x=10, y=165)

root.mainloop()