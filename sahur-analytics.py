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
from colorama import init, Fore, Back, Style
from pythonping import ping

version = "v 1.2 / 15.10.2026"

init()
#os.system('mode con: cols=45 lines=6')

time_now = "none"
ping_now = "none"
public_ip = "none"
local_ip = "none"
datetime_now = "none"
valutes = {'eur':'none', 'usd':'none', 'cny':'none'}
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
    path = '/'
    usage = shutil.disk_usage(path) 
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
            valutes['eur'] = str(data['Valute']["EUR"]['Value'])[0:5]
            valutes['usd'] = str(data['Valute']["USD"]['Value'])[0:5]
            valutes['cny'] = str(data['Valute']["CNY"]['Value'])[0:5]
            return "yea"
    else: return "Ошибка подключения к серверу"

def time_info():
    global time_now
    time_now = str(datetime.datetime.now())[:-7]

def ping_info():
    response = ping("8.8.8.8", count=1) # ICMP-запросы
    response = str(response.rtt_avg_ms)
    if len(response) < 5: response = response + "0"
    if len(response) > 5: response = response[:-1]
    global ping_now; ping_now = response


# функция мониторинга интернет соеденения 
# мониторинг задержки
# мониторинг связи узлов
# мониторинг места на диске

print(Fore.WHITE, '   sahur-system-[2] / '+ version, Fore.RESET) 

def vew_data():
    # Код \033[K очищает строку от курсора до конца (чтобы не оставалось хвостов)
    LINE_01   = f"   _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _  \033[K"
    LINE_02   = f"  / \033[36m{time_now              }\033[0m / EUR {valutes['eur']} / {disk_data['vsego']}   / \033[K"
    LINE_03   = f" / \033[32mЗадержка: {ping_now} ms\033[0m  / USD {valutes['usd']} / {disk_data['zanyato']}  / \033[K"
    LINE_04   = f"/ \033[33m{disk_data['svobodno']}\033[0m  / CNY {valutes['cny']} / {disk_data['svobodno']} / \033[K"
    # Выводим рамку
    print(LINE_01)
    print(LINE_02)
    print(LINE_03)
    print(LINE_04, end="", flush=True)
    # Магия: возвращаем курсор на 3 строки вверх, чтобы перезаписать рамку
    # \033[3F поднимает курсор в начало строки на 3 уровня выше
    # \r сдвигает курсор в самый левый край текущей (нижней) строки
    print("\r\033[3F", end="", flush=True)

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
  except KeyboardInterrupt: return "exit"
  #except: pass   

def main(): 
  setup_data()
  while True:
    time.sleep(1)
    update_data_on_time()
    vew_data()

if __name__ == "__main__":
   main()


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


print('exit')