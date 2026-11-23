# sahur-system-[2] / v-1.0 / 19.07.2026 - analytics 

from os import system as os_system, path as os_path
from sys import platform as sys_platform
from subprocess import check_output as subprocess_check_output
from shutil import disk_usage as shutil_disk_usage
import socket
import requests
import time
import datetime
import string
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


def ip_addresses():
    global public_ip, local_ip
    try: # белый айпи
      public_ip = requests.get('https://ifconfig.me', timeout=5).text.strip()
    except requests.RequestException as e: public_ip = f"Ошибка при получении белого IP: {e}"
    try: # серый айпи
      hostname = socket.gethostname()
      local_ip = socket.gethostbyname(hostname)
    except: local_ip = 'Ошибка при получении локального IP'
    if len(local_ip) < 15: 
        local_ip = local_ip + (" " * (15 - len(local_ip)))
    if len(public_ip) < 15: 
        public_ip = public_ip + (" " * (15 - len(public_ip)))
    public_ip = '173.92.217.22  '

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
    weather = f"{current['temp_C'][:2]}°C  {current['humidity'][:2]}%  {current['windspeedKmph'][:2]}км/ч"

  except requests.RequestException as e: 
     weather = "request error"; 
     print(f"[weather] request error : {e} \n")


def disk_info():
    path = '/'
    usage = shutil_disk_usage(path) 
    gb = 2 ** 30 # байты в гигабайты
    disk_data['vsego'] = f"{usage.total / gb:.2f}"[:6]
    disk_data['zanyato'] = f"{usage.used / gb:.2f}"[:6]
    disk_data['svobodno'] = f"{usage.free / gb:.2f}"[:6]

    if len(disk_data['vsego']) < 6: disk_data['vsego'] = ('0'*(6-len(disk_data['vsego'])))+disk_data['vsego']
    if len(disk_data['zanyato']) < 6: disk_data['zanyato'] = ('0'*(6-len(disk_data['zanyato'])))+disk_data['zanyato']
    if len(disk_data['svobodno']) < 6: disk_data['svobodno'] = ('0'*(6-len(disk_data['svobodno'])))+disk_data['svobodno']

    if len(disk_data['vsego']) > 6: disk_data['vsego'] = disk_data['vsego'][:(6 - len(disk_data['vsego']))]
    if len(disk_data['zanyato']) > 6: disk_data['zanyato'] = disk_data['zanyato'][:(6 - len(disk_data['zanyato']))]
    if len(disk_data['svobodno']) > 6: disk_data['svobodno'] = disk_data['svobodno'][:(6 - len(disk_data['svobodno']))]

    global disks_list, disk_name
    disks_list = [f"{letter}:\\" for letter in string.ascii_uppercase if os_path.exists(f"{letter}:\\")]

    disk_name = subprocess_check_output("cmd /c echo %CD:~0,2%", text=True).strip()


def disk_info():
    path = '/'
    usage = shutil_disk_usage(path) 
    gb = 2 ** 30 # байты в гигабайты
    disk_data['vsego'] = f"{usage.total / gb:.2f}"[:6]
    disk_data['zanyato'] = f"{usage.used / gb:.2f}"[:6]
    disk_data['svobodno'] = f"{usage.free / gb:.2f}"[:6]

    if len(disk_data['vsego']) < 6: disk_data['vsego'] = ('0'*(6-len(disk_data['vsego'])))+disk_data['vsego']
    if len(disk_data['zanyato']) < 6: disk_data['zanyato'] = ('0'*(6-len(disk_data['zanyato'])))+disk_data['zanyato']
    if len(disk_data['svobodno']) < 6: disk_data['svobodno'] = ('0'*(6-len(disk_data['svobodno'])))+disk_data['svobodno']

    if len(disk_data['vsego']) > 6: disk_data['vsego'] = disk_data['vsego'][:(6 - len(disk_data['vsego']))]
    if len(disk_data['zanyato']) > 6: disk_data['zanyato'] = disk_data['zanyato'][:(6 - len(disk_data['zanyato']))]
    if len(disk_data['svobodno']) > 6: disk_data['svobodno'] = disk_data['svobodno'][:(6 - len(disk_data['svobodno']))]

    global disks_list, disk_name
    disks_list = [f"{letter}:\\" for letter in string.ascii_uppercase if os_path.exists(f"{letter}:\\")]

    disk_name = subprocess_check_output("cmd /c echo %CD:~0,2%", text=True).strip()

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
    pingRequest = ping("8.8.8.8", count=1) # ICMP-запросы
    response = str(pingRequest.rtt_avg_ms)

    if len(response) < 5: 
       if len(response) < 2:
          response = '0'+ response + '.'+("0"*(5 - len(response)))
       else: response = response + '.'+("0"*(5 - len(response)))
    if len(response) > 5: response = response[:(5 - len(response))]
    global ping_now; ping_now = response


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
    label_PING.config(text=f"ping : {ping_now}")

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

  label_TIME = tkinter.Label(root, text=time_now,width=18, height=1, font=("Arial", 9)) # -------------- Время
  label_TIME.place(x=210, y=10)

  label_PING = tkinter.Label(root, text=f"ping : {ping_now}") # ---------------------------------------- Пинг
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

  name_disk_tab = tkinter.Label(root, text=" Диск: "+disk_name) # ------------------------------------------------- Диски
  name_disk_tab.place(x=125, y=100)
  vse = tkinter.Label(root, text=f"Всего: {disk_data['vsego']}")
  vse.place(x=125, y=125)
  zan = tkinter.Label(root, text=f"Занято: {disk_data['zanyato']}")
  zan.place(x=125, y=148)
  svo = tkinter.Label(root, text=f"Свободно: {disk_data['svobodno']}")
  svo.place(x=125, y=171)

  label_weather = tkinter.Label(root, text="Погода") # ------------------------------------------------- Погода
  label_weather.place(x=125, y=40)
  label_weather = tkinter.Label(root, text=weather)
  label_weather.place(x=125, y=65)


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