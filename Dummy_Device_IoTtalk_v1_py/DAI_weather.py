# DAI2.py #coding=utf-8 -- new version of Dummy Device DAI.py, modified by tsaiwn@cs.nctu.edu.tw
import time, DAN, requests, random 
import threading, sys # for using a Thread to read keyboard INPUT

# week10
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime
###

# ServerURL = 'http://Your_server_IP_or_DomainName:9999' #with no secure connection
#  注意你用的 IoTtalk 伺服器網址或 IP  #  https://goo.gl/6jtP41

ServerURL = 'https://7.iottalk.tw/' # with SSL secure connection

# ServerURL = 'https://Your_DomainName' #with SSL connection  (IP can not be used with https)
Reg_addr = None #if None, Reg_addr = MAC address #(本來在 DAN.py 要這樣做 :-) 
# Note that Reg_addr 在以下三句會被換掉! # the mac_addr in DAN.py is NOT used
mac_addr = 'CD8600D38' + str( random.randint(100,999 ) )  # put here for easy to modify :-)
# 若希望每次執行這程式都被認為同一個 Dummy_Device, 要把上列 mac_addr 寫死, 不要用亂數。
Reg_addr = mac_addr   # Note that the mac_addr generated in DAN.py always be the same cause using UUID !
DAN.profile['dm_name']='Weather_Station'   # you can change this but should also add the DM in server
DAN.profile['df_list']=['date', 'temp', 'weather', 'wind_speed', 'visible', 'hum', 'rain']   # Check IoTtalk to see what IDF/ODF the DM has
DAN.profile['d_name']= "087_WS."+ str( random.randint(100,999 ) ) +"_"+ DAN.profile['dm_name'] # None

DAN.device_registration_with_retry(ServerURL, Reg_addr) 
print("dm_name is ", DAN.profile['dm_name']) ; print("Server is ", ServerURL);
# global gotInput, theInput, allDead    ## 主程式不必宣告 globel, 但寫了也 OK
gotInput=False
theInput="haha"
allDead=False

date, temp, weather, wind_speed, visible, hum, rain = [], [], [], [], [], [], []
def doRead( ):
   global date, temp, weather, wind_speed, visible, hum, rain
   url = 'https://www.cwb.gov.tw/V8/C/W/OBS_Station.html?ID=46757'
   options = Options()
   options.add_argument('--headless')
   driver = webdriver.Chrome(options=options)
   driver.get(url)
   soup = BeautifulSoup(driver.page_source, features='lxml')
   tbody = soup.find('tbody', {'id':'obstime'})
   trs = tbody.find_all('tr')
   
   year = str(datetime.datetime.now().year)
   for tr in trs:
      d = tr.th.text
      d = year + d
      # date.append(datetime.datetime.strptime(d,'%Y%m/%d %H:%M'))
      # weather.append(tr.find('td', {'headers':'weather'}).find('img')['title'])
      temp.append(tr.find('td', {'headers':'temp'}).text)
      # wind_speed.append(tr.find('td', {'headers':'w-2'}).text)
      # visible.append(tr.find('td', {'headers':'visible-1'}).text)
      # hum.append(tr.find('td', {'headers':'hum'}).text)
      # rain.append(tr.find('td', {'headers':'rain'}).text)
      break
   driver.quit()
     

#creat a thread to do Input data from keyboard, by tsaiwn@cs.nctu.edu.tw 
threadx = threading.Thread(target=doRead)
threadx.daemon = True  # 這樣才不會阻礙到主程式的結束
threadx.start()


pre_time = 0
wait = 20
while True:
   try:
      if(allDead): break;
   #Pull data from a device feature called "Dummy_Control"
      cur_time = time.time()
      if cur_time - pre_time >= wait:
         doRead()
         print(date[-1], temp[-1], weather[-1], wind_speed[-1], visible[-1], hum[-1], rain[-1])
         DAN.push('date', 'date: ' + str(date[-1]))
         time.sleep(1)
         DAN.push('temp', 'temp: ' + str(temp[-1]))
         time.sleep(1)
         DAN.push('weather', 'weather: ' + str(weather[-1]))
         time.sleep(1)
         DAN.push('wind_speed', 'wind_speed: ' + str(wind_speed[-1]))
         time.sleep(1)
         DAN.push('visible', 'visible: ' + str(visible[-1]))
         time.sleep(1)
         DAN.push('hum', 'hum: ' + str(hum[-1]))
         time.sleep(1)
         DAN.push('rain', 'rain: ' + str(rain[-1]))
         time.sleep(1)
         pre_time = cur_time
      
   except Exception as e:
      print(e)
      if str(e).find('mac_addr not found:') != -1:
         print('Reg_addr is not found. Try to re-register...')
         DAN.device_registration_with_retry(ServerURL, Reg_addr)
      else:
         print('Connection failed due to unknow reasons.')
         time.sleep(1)    
   try:
      time.sleep(0.2)
   except KeyboardInterrupt:
      break
time.sleep(0.25)
try: 
   DAN.deregister()    # 試著解除註冊
except Exception as e:
   print("===")
print("Bye ! --------------", flush=True)
sys.exit( );