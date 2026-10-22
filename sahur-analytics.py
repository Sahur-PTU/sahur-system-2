# sahur-system-[2] / v-1.0.1 / 22.10.2026 - analytics 

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
from colorama import init, Fore, Back, Style
from pythonping import ping


init()
os.system('mode con: cols=45 lines=6')

print(Fore.WHITE,'sahur-system-[2] / v-1.0 / 19.07.2026',Style.RESET_ALL) 

time_now = "none"
ping_now = "none"
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
    usage = shutil.disk_usage(path) 
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

def _time():
    global time_now
    time_now = str(datetime.datetime.now())[:-7]

def _ping():
    response = ping("8.8.8.8", count=4) # ICMP-запросы
    r = str(response.rtt_avg_ms)
    if len(r) < 5: r = r + " "
    if len(r) > 5: r = r[:-1]
    global ping_now; ping_now = r


# функция мониторинга интернет соеденения 
# мониторинг задержки
# мониторинг связи узлов
# мониторинг места на диске


def vew_data():
    # Код \033[K очищает строку от курсора до конца (чтобы не оставалось хвостов)
    LINE_01   = f"   _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ \033[K"
    LINE_02   = f"  / \033[36m{time_now}\033[0m / EUR {valutes['eur']}  \033[K"
    LINE_03   = f" / \033[32mЗадержка: {ping_now}\033[0m     / USD {valutes['usd']}  \033[K"
    LINE_04   = f"/ \033[33m{disk_data['svobodno']}\033[0m  / CNY {valutes['cny']}  \033[K"
    # Выводим рамку
    print(LINE_01)
    print(LINE_02)
    print(LINE_03)
    print(LINE_04, end="", flush=True)
    # Магия: возвращаем курсор на 3 строки вверх, чтобы перезаписать рамку
    # \033[3F поднимает курсор в начало строки на 3 уровня выше
    # \r сдвигает курсор в самый левый край текущей (нижней) строки
    print("\r\033[3F", end="", flush=True)


def update_data_new():
  loop = 10
  while True: 
    loop += 1
    time.sleep(1)
    try:
        get_time = _time()
        if loop % 2: 
          get_ping = _ping()
        if loop > 10: 
          loop = 0
          get_disk = disk()
          valutes_s = get_currency_rate()
        vew_data()
        #print(f"\r {time_now}   {ping_now}  {disk_data}", end="", flush=False)
    except IndexError: print('indexError')
    except KeyboardInterrupt: return "exit"
    #except: pass   

update_data_new()
exit()

def menu():
    while True:
      #os.system('cls'), time.sleep(1)
      print('\n'+local_ip)
      print(public_ip)
      while True:
        try:
          datetime_now = str(datetime.datetime.now())[:-7]
          host = '8.8.8.8' 
          response = ping(host, count=4) # ICMP-запросы
          print(f"{datetime_now} / {response.rtt_avg_ms} мс",end="\r",flush=True),time.sleep(1)
        except KeyboardInterrupt: exit()

a = menu()

print('exit')
