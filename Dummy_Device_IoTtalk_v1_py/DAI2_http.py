# DAI2.py #coding=utf-8 -- new version of Dummy Device DAI.py, modified by tsaiwn@cs.nctu.edu.tw
import time, DAN, requests, random 
import threading, sys # for using a Thread to read keyboard INPUT

# ServerURL = 'http://Your_server_IP_or_DomainName:9999' #with no secure connection
#  注意你用的 IoTtalk 伺服器網址或 IP  #  https://goo.gl/6jtP41

ServerURL = 'https://7.iottalk.tw/' # with SSL secure connection

# ServerURL = 'https://Your_DomainName' #with SSL connection  (IP can not be used with https)
Reg_addr = None #if None, Reg_addr = MAC address #(本來在 DAN.py 要這樣做 :-) 
# Note that Reg_addr 在以下三句會被換掉! # the mac_addr in DAN.py is NOT used
mac_addr = 'CD8600D38' + str( random.randint(100,999 ) )  # put here for easy to modify :-)
# 若希望每次執行這程式都被認為同一個 Dummy_Device, 要把上列 mac_addr 寫死, 不要用亂數。
Reg_addr = mac_addr   # Note that the mac_addr generated in DAN.py always be the same cause using UUID !
DAN.profile['dm_name']='Dummy_Device'   # you can change this but should also add the DM in server
DAN.profile['df_list']=['Dummy_Sensor', 'Dummy_Control']   # Check IoTtalk to see what IDF/ODF the DM has
DAN.profile['d_name']= "SYC_087."+ str( random.randint(100,999 ) ) +"_"+ DAN.profile['dm_name'] # None

DAN.device_registration_with_retry(ServerURL, Reg_addr) 
print("dm_name is ", DAN.profile['dm_name']) ; print("Server is ", ServerURL);
# global gotInput, theInput, allDead    ## 主程式不必宣告 globel, 但寫了也 OK
gotInput=False
theInput="haha"
allDead=False

##############
time.sleep(10)
late_data = []

while True:
   if len(late_data) == 100:
         print('avg latency:', sum(late_data) / len(late_data))
         break
   upload_data = random.uniform(1, 100)
   start = time.perf_counter()
   DAN.push('Dummy_Sensor', upload_data)
   print('push', len(late_data), 'data')
   
   while True:
      try:
         if(allDead): break
      #Pull data from a device feature called "Dummy_Control"
         value1 = DAN.pull('Dummy_Control')
         print(value1, upload_data)
         if value1 != None and value1[0] == upload_data:    # 不等於 None 表示有抓到資料
            print ('got data:', value1)
            late_data.append(time.perf_counter() - start)
            print(late_data[-1])
            break

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
sys.exit( )