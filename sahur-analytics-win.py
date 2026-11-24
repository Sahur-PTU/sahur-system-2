# sahur-system-[2] / v-1.2 / 24.11.2026 - analytics / anatoly and caktuz

from os import system as os_system, path as os_path
from sys import platform as sys_platform
from subprocess import check_output as subprocess_check_output
from shutil import disk_usage as shutil_disk_usage
from pathlib import Path
import psutil
import socket
import requests
import time
import datetime
import tkinter
from colorama import init as colorama_init, Fore, Back, Style
from pythonping import ping


time_now = "none"
ping_now = "none"
public_ip = "none"
local_ip = "none"
datetime_now = "none"
valutes = {'eur':'none', 'usd':'none', 'cny':'none'}
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
    global weather
    params = {
       "latitude": 55.7558,
       "longitude": 37.6173,
       "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
       "timezone": "Europe/Moscow", 
      }
    
    url = "https://wttr.in"
    params = {"format": "j1", "lang": "ru"}
    headers = {"User-Agent": "curl/8.0"}

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    current = data["current_condition"][0]
    weather = f"{current['temp_C'][:2]}°C  {current['humidity'][:2]}%  {str(int(current['windspeedKmph'])/3.6)[:3]}м/c"

    if len(weather) < 18: # форматирование 
      raznica = 18 - len(weather)
      num_1 = raznica // 2 
      num_2  = raznica - num_1
      weather = (' ' * num_1) + weather + (' ' * num_2)

  except requests.RequestException as e:
     weather = "request error     "; 
     print(f"[weather] request error : {e} \n")
  except: weather  = "something error   "

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

    partitions = psutil.disk_partitions()
    for p in partitions: 
       if p.fstype == 'NTFS': disks_list.append(p.device)

    disks_count = len(disks_list)

    current_path = Path(__file__).resolve()
    disk_name = current_path.anchor

  #except: disks_count = 0

def currency_rate():
  try:
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    response = requests.get(url)
    if response.status_code == 200:
            data = response.json()
        # Поиск курса валюты по её коду (например, USD или EUR)
            valutes['eur'] = str(data['Valute']["EUR"]['Value'])[0:6]
            valutes['usd'] = str(data['Valute']["USD"]['Value'])[0:6]
            valutes['cny'] = str(data['Valute']["CNY"]['Value'])[0:6]
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
    pingRequest = ping("8.8.8.8", count=1) # ICMP-запросы
    response = str(pingRequest.rtt_avg_ms)

    if len(response) < 5: # форматирование 
        if len(response) < 2: 
            response = '0'+ response
        if '.' not in response:
            response = response + '.' + ("0" * (5 - len(response)))
        else: response = response + ("0" * (5 - len(response)))
      
    global ping_now; ping_now = response[:5]
  except: ping_now = 'ERROR'


# функция мониторинга интернет соеденения 
# мониторинг задержки
# мониторинг связи узлов
# мониторинг места на диске

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
          get_weather = weather_info()
          valutes_s = currency_rate()
  except IndexError: print('indexError')
  except KeyboardInterrupt: return 0
  #except: pass   



def window():
  def update_data():
    update_data_on_time() # обновляем данные
    # обновляем текст в метках
    label_TIME.config(text=time_now)
    label_PING.config(text=f"ping : {ping_now} ms ")

    # Планируем следующий вызов этой же функции через 800 мс
    root.after(800, update_data)

  
  def write(): # бурда просто типа писать в файл и читать из него
    with open('output.txt', 'w') as file:
       file.write(entry.get())
  def read():
    try:
      with open('output.txt', 'r') as file:
        r = tkinter.Label(root, text=file.read())
        r.place(x=10,y=120)
    except FileNotFoundError: print("файл не найден")

  root = tkinter.Tk() # создание окна
  root.title("Sahur Analytics")
  #root.iconbitmap(r"")
  root.geometry("350x200")
  root.wm_attributes('-alpha', 0.9)
  root.configure(bg="#584e4e") # или root['bg'] = 'blue'

  root.after(1000, update_data) # обновление данных

  label_TIME = tkinter.Label(root, text=time_now,width=18, height=1, font=("Arial", 9)) # -------------- Время
  label_TIME.place(x=210, y=10)

  label_PING = tkinter.Label(root, text=f"ping : {ping_now} ms ") # ------------------------------------ Пинг
  label_PING.place(x=250, y=95)

  
  label_LOCAL_IP = tkinter.Label(root, text="L IP: "+local_ip) # --------------------------------------- Айпишки
  label_LOCAL_IP.place(x=232, y=40)
  label_PUBLIC_IP = tkinter.Label(root, text="P IP: "+public_ip)
  label_PUBLIC_IP.place(x=232, y=65)

  label_EUR = tkinter.Label(root,text=f"EUR : {valutes['eur']}", width=12, height=1,font=("Arial", 9)) # Валюты
  label_EUR.place(x=250, y=125)
  label_USD = tkinter.Label(root,text=f"USD : {valutes['usd']}", width=12, height=1,font=("Arial", 9))
  label_USD.place(x=250, y=148)
  label_CNY = tkinter.Label(root,text=f"CNY : {valutes['cny']}", width=12, height=1,font=("Arial", 9))
  label_CNY.place(x=250, y=171)

  tab_DISKS_COUNT = tkinter.Label(root, text=f" Дисков: {disks_count} шт") # --------------------------- Диски
  tab_DISKS_COUNT.place(x=75, y=95)
  label_TEKUSHIY = tkinter.Label(root, text=f"Текущий: {disk_name} ")
  label_TEKUSHIY.place(x=160, y=95)
  label_SVO = tkinter.Label(root, text=f"Свободно: {disk_data['svobodno']} из {disk_data['vsego']} GB")
  label_SVO.place(x=75, y=120)

  tab_WEATHER = tkinter.Label(root, text="Погода") # --------------------------------------------------- Погода
  tab_WEATHER.place(x=120, y=40)
  label_WEATHER = tkinter.Label(root, text=weather)
  label_WEATHER.place(x=120, y=65)


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

    except KeyboardInterrupt: return 1

_main = main()