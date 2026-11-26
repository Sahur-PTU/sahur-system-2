# sahur-system-[2] / v-1.2 / 25.11.2026 - analytics / anatoly and caktuz

from os import system as os_system, path as os_path
from sys import platform as sys_platform
from subprocess import check_output as sbprc_check_output
from shutil import disk_usage as shutil_disk_usage
from pathlib import Path
import socket

import psutil
import requests
from icmplib import ping
from colorama import init as colorama_init, Fore, Back, Style

import time
import datetime


version = "v 1.2 / 25.11.2026"
colorama_init()
#os_system('mode con: cols=45 lines=6')

if sys_platform == "win32": clearOutput = 'cls'
else: clearOutput = 'clear'


time_now = "none"
ping_now = "none"
public_ip = "none"
local_ip = "none"
datetime_now = "none"
valutes = {'eur':'none', 'usd':'none', 'cny':'none'}
weather = "none"
disk_data = {'vsego':'none','zanyato':'none','svobodno':'none'}
disk_name = "/"
disks_list = []
disks_count = 0


def ip_addresses():
  try:
    global public_ip, local_ip
    try: # белый айпи
      public_ip = requests.get('https://ifconfig.me', timeout=5).text.strip()
    except requests.RequestException as e: public_ip = f"Ошибка при получении белого IP: {e}"
    try: # серый айпи
      hostname = socket.gethostname()
      local_ip = socket.gethostbyname(hostname)
    except: local_ip = 'Ошибка при получении локального IP'

    public_ip = '173.92.217.22'
    if len(local_ip) < 15: # форматирование 
        local_ip = local_ip + (" " * (15 - len(local_ip)))
    if len(public_ip) < 15: 
        public_ip = public_ip + (" " * (15 - len(public_ip)))

    local_ip = local_ip[:15]
    public_ip = public_ip[:15]
  except: 
    public_ip = 'RROR ERROR ERRO'
    return False
  

def weather_info():
  try:
    global weather, public_ip
 
    # Определение координат по IP через ipwho.is (работает по HTTPS без ключа)
    req_ip_crd = requests.get(f"https://ipinfo.io/{public_ip.strip()}/json", timeout=5) # запрашиваем геоданные
    geo_data = req_ip_crd.json()

    x, y = geo_data['loc'].split(",")
    city = geo_data.get("city")

    # запрос по полученным координатам
    weather_url = (
      f"https://api.open-meteo.com/v1/forecast?"
      f"latitude={x}&longitude={y}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
    )

    req_weather = requests.get(weather_url, timeout=5) # запрашиваем погоду
    weather_data = req_weather.json()

    current = weather_data["current"]
    weather = f"{current['temperature_2m']}°C {current['relative_humidity_2m']}% {str(current["wind_speed_10m"]/3.6)[:3]}м/с"
      
    if len(weather) < 18: # форматирование 
      raznica = 18 - len(weather)
      num_1 = raznica // 2 
      num_2  = raznica - num_1
      weather = (' ' * num_1) + weather + (' ' * num_2)

  except requests.RequestException as e:
     weather = "request error     "; 
     #print(f"[weather] request error : {e} \n")
  #except: weather  = "something error   "

  weather = weather[:18]


def disk_info():
  #try:
    path = '/'
    usage = shutil_disk_usage(path) 
    gb = 2 ** 30 # байты в гигабайты
    disk_data['vsego'] = f"{usage.total / gb:.2f}"[:6]
    disk_data['zanyato'] = f"{usage.used / gb:.2f}"[:6]
    disk_data['svobodno'] = f"{usage.free / gb:.2f}"[:6] 
    
    for el in disk_data: # форматирование
      if len(disk_data[el]) < 6: 
        disk_data[el] = (' ' * (4-len(disk_data[el]))) + disk_data[el]
            
        if '.' not in disk_data[el] and len(disk_data[el]) < 5:
            disk_data[el] =  disk_data[el] + '.' + ('0' * (6-len(disk_data[el])))
        else: 
            disk_data[el] =  ('0' * (6-len(disk_data[el]))) + disk_data[el] 
      disk_data[el] = disk_data[el][:6]


    global disks_list, disk_name, disks_count

    disks_plenty = []
    partitions = psutil.disk_partitions()
    for p in partitions: 
       if p.fstype == 'NTFS': disks_plenty.append(p.device)
    disks_list = list(disks_plenty) # перезапись шобы не дублировались элементы

    """if sys_platform == "win32": # это типа имена накопителей получать 
        cmd = ["powershell","-NoProfile","-Command","Get-PhysicalDisk | Select-Object -ExpandProperty FriendlyName",]
        output = check_output(cmd, text=True).strip() 
        disks_list = [line.strip() for line in output.splitlines() if line.strip()]"""

    if sys_platform.startswith("linux"):
        # lsblk -d выводит только сами устройства (без разделов sda1, sda2 и т.д.)
        cmd = ["lsblk", "-d", "-n", "-o", "NAME,TYPE"]  # -n убирает заголовки, -o NAME,TYPE выводит имя и тип
        output = sbprc_check_output(cmd, text=True).strip()
        disks_list = [ # Фильтрация. только тип 'disk' (отсекает loop-устройства и CD-ROM)
            line.split()[0]
            for line in output.splitlines()
            if line.endswith("disk")
        ]

    disks_count = len(disks_list)
    
    current_path = Path(__file__).resolve()
    disk_name = current_path.anchor

    if len(disk_name) < 3:
       disk_name = disk_name + (" " * (3-len(disk_name)))[:3]

  #except: disks_count = 0

def currency_rate():
  try:
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    response = requests.get(url)
    if response.status_code == 200:
            data = response.json()
        # Поиск курса валюты по её коду (например, USD или EUR)
            valutes['eur'] = str(data['Valute']["EUR"]['Value'])[0:5]
            valutes['usd'] = str(data['Valute']["USD"]['Value'])[0:5]
            valutes['cny'] = str(data['Valute']["CNY"]['Value'])[0:5]
            return True
    else: 
       for valute in valutes: valutes[valute] = 'error'
       return "Ошибка подключения к серверу"
  except: 
     for valute in valutes: valutes[valute] = 'ERROR'
     return "Ошибка подключения к серверу"
       

def time_info():
    global time_now
    time_now = str(datetime.datetime.now())[:-7]

def ping_info():
  try:
   # privileged=False позволяет запускать без прав root/администратора
    response = ping("8.8.8.8", count=2, interval=0.2, timeout=3, privileged=False) # ICMP-запросы
    
    if response.is_alive:
       response = str(response.avg_rtt)[:5]
    else: response = "ERROR"

    if len(response) < 5: # форматирование 
        if len(response) < 2: 
            response = '0'+ response
        if '.' not in response:
            response = response + '.' + ("0" * (5 - len(response)))
        else: response = response + ("0" * (5 - len(response)))

    global ping_now; ping_now = response[:5]

  except: ping_now = 'ERROR'


def vew_table():
    # Код \033[K очищает строку от курсора до конца (чтобы не оставалось хвостов)
    LINE_01   = f" /\ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\ \033[K"
    LINE_02   = f"/ /\033[36m {time_now              } \033[0m/ EUR {valutes['eur']} /\033[35m Дисков: {disks_count} шт. Текущий: {disk_name} \033[0m/ \033[K"
    LINE_03   = f" /\033[32m Задержка: {ping_now} ms  \033[0m/ USD {valutes['usd']} /\033[34m Места: {disk_data['svobodno']} из {disk_data['vsego']} GB \033[0m/ \033[K"
    LINE_04   = f"/\033[33m IP: {public_ip         } \033[0m/ CNY {valutes['cny']} /\033[36m Погода: {weather} \033[0m/ \033[K"
    print(LINE_01)
    print(LINE_02)
    print(LINE_03)
    print(LINE_04, end="", flush=True)
    # \033[3F поднимает курсор в начало строки на 3 уровня выше
    # \r сдвигает курсор в самый левый край текущей (нижней) строки
    print("\r\033[3F", end="", flush=True)

def setup_data():
  get_ip_addreses = ip_addresses()
  get_valutes = currency_rate()
  get_weather = weather_info()
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
      if loop >= 60: 
          loop = 0
          valutes_s = currency_rate()
          get_weather = weather_info()
  except IndexError: print('indexError')
  except KeyboardInterrupt: return "exit"
  

def main(): 
  try:
    os_system(clearOutput)
    setup_data()
    print(Fore.WHITE, ' _ _ sahur-system-[2] / '+ version +' _ _ _ _ _ _ _ _ _ _ _ ', Fore.RESET) 
    while True:
      update_data_on_time()
      #time.sleep(2)
      vew_table()
      time.sleep(1)
  except KeyboardInterrupt: return 1

if __name__ == "__main__":
   main()


def menu(): # древние наскальные рисунки
    while True:
      #os.system('cls'), time.sleep(1)
      print('\n'+local_ip)
      print(public_ip)
      while True:
        try:
          datetime_now = str(datetime.datetime.now())[:-7]
          host = '8.8.8.8' 
          response = ping(host, count=4) # ICMP-запросы
          print(f"{datetime_now} / {response.rtt_avg_ms} мс",end="\r",flush=True);time.sleep(1)
        except KeyboardInterrupt: return 
      print('exit')