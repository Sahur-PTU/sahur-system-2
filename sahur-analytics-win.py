# sahur-system-[2] / v-1.0 / 19.07.2026 - analytics 

import os
from sys import platform
#import subprocess
#import json
#import webbrowser
import shutil
import socket
import requests
import time
import datetime
import tkinter
#import threading
from pythonping import ping


time_now = "none"
ping_now = "none"
public_ip = "none"
local_ip = "none"
datetime_now = "none"
valutes = {'eur':'none', 'usd':'none', 'cny':'none'}
disk_name = "/"
disk_data = {'vsego':'none','zanyato':'none','svobodno':'none'}


def ip_addresses():
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

def disk_info():
    global disk_name
    usage = shutil.disk_usage(disk_name) # получаем информацию о диске
    gb = 2 ** 30 # байты в гигабайты
    disk_data['vsego'] = f"Всего: {usage.total / gb:.2f} GB"
    disk_data['zanyato'] = f"Занято: {usage.used / gb:.2f} GB"
    disk_data['svobodno'] = f"Свободно: {usage.free / gb:.2f} GB"

def currency_rate():
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    response = requests.get(url)
    if response.status_code == 200:
            data = response.json()
        # Поиск курса валюты по её коду (например, USD или EUR)
            valutes['eur'] = str(data['Valute']["EUR"]['Value'])[:6]
            valutes['usd'] = str(data['Valute']["USD"]['Value'])[:6]
            valutes['cny'] = str(data['Valute']["CNY"]['Value'])[:6]
            return "yea"
    else: return "Ошибка подключения к серверу"

def time_info():
    global time_now
    time_now = str(datetime.datetime.now())[:-7]

def ping_info():
    pingRequest = ping("8.8.8.8", count=4) # ICMP-запросы
    response = str(pingRequest.rtt_avg_ms)
    if len(response) < 5: response = response + "0"
    if len(response) > 5: response = response[:-1]
    global ping_now; ping_now = response

# функция мониторинга интернет соеденения 
# мониторинг задержки
# мониторинг связи узлов
# мониторинг места на диске

def setup_data():
  get_ip_addreses = ip_addresses()
  get_valutes = currency_rate()
  get_time = time_info()
  get_ping = ping_info()
  get_disk = disk_info()

loop = 0
def update_data_on_time():
  global loop
  loop += 1
  try:
      get_time = time_info()
      if loop % 2: 
          get_ping = ping_info()
      if loop == 10: 
          get_disk = disk_info()
      if loop >= 30: 
          loop = 0
          valutes_s = currency_rate()
  except IndexError: print('indexError')
  except KeyboardInterrupt: return 0
  #except: pass   



def window():
  def update_data():
    update_data_on_time() # обновляем данные
    # обновляем текст в метках
    time_output.config(text=time_now)
    ping_output.config(text=f"ping : {ping_now}")

    # Планируем следующий вызов этой же функции через 800 мс
    root.after(800, update_data)

  
  def write():
    with open('data/output.txt', 'w') as file:
       file.write(entry.get())
  def read():
    try:
      with open('data/output.txt', 'r') as file:
        r = tkinter.Label(root, text=file.read())
        r.place(x=10,y=120)
    except FileNotFoundError: print("файл не найден")

  root = tkinter.Tk() # создание окна
  root.title("Sahur Analytics")
  #root.iconbitmap(r"")
  root.geometry("350x200")
  root.wm_attributes('-alpha', 0.9)
  root.configure(bg="#584e4e") # или root['bg'] = 'blue'

  root.after(800, update_data) # обновление данных

  time_output = tkinter.Label(root, width=18, height=1, font=("Arial", 9))
  time_output.place(x=210, y=10)

  ping_output = tkinter.Label(root, text=f"ping : {ping_now}")    
  ping_output.place(x=250, y=95)
  

  label_local_ip = tkinter.Label(root, text="L IP: "+local_ip)
  label_local_ip.place(x=232, y=40)
  label_public_ip = tkinter.Label(root, text="P IP: "+public_ip)
  label_public_ip.place(x=231, y=65)

  eur_label = tkinter.Label(root,text=f"EUR : {valutes['eur']}", width=12, height=1,font=("Arial", 9))    
  eur_label.place(x=250, y=125)
  usd_label = tkinter.Label(root,text=f"USD : {valutes['usd']}", width=12, height=1,font=("Arial", 9))
  usd_label.place(x=250, y=148)
  cny_label = tkinter.Label(root,text=f"CNY : {valutes['cny']}", width=12, height=1,font=("Arial", 9))
  cny_label.place(x=250, y=171)

  name_disk_tab = tkinter.Label(root, text=" Диск ")
  name_disk_tab.place(x=125, y=100)
  vse = tkinter.Label(root, text=disk_data['vsego'])
  vse.place(x=125, y=125)
  zan = tkinter.Label(root, text=disk_data['zanyato'])
  zan.place(x=125, y=148)
  svo = tkinter.Label(root, text=disk_data['svobodno'])
  svo.place(x=125, y=171)


  btn_1 = tkinter.Button(root, text='Чтение', command=read)
  btn_1.place(x=10, y=40)
  btn_1 = tkinter.Button(root, text='Выйти', command=root.destroy)
  btn_1.place(x=10, y=10)

  entry = tkinter.Entry(root, width=15)
  entry.place(x=10, y=145)
  button = tkinter.Button(root, text="запись",width=12, command=write)
  button.place(x=10, y=165)

  root.mainloop()



def settings(): # потом доделаю
  print("""
enter : «disk <name>» to change disk
        «none»""")
  set_data = input('>> ') 
   
  if set_data.startswith('disk '):
    if set_data[-1:] in ('C','c','D','d','E','e','F','f'):
        global disk_name
        disk_name = set_data[-1:]+':/'
        print('disk',disk_name)
        print('saved')
   


def main() :
  #while True:
    time.sleep(0.5)
    try: 
        setup_data()

        #settings()
        
        #t1 = threading.Thread(target=loop_update_data) # пока пусть будет
        #t1.start()

        _window = window()

        #t1.join()

    except KeyboardInterrupt: return "exit"

_main = main()