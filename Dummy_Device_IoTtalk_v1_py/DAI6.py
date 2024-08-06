# DAI6.py #coding=utf-8 --  Dummy Device with Tk Slider, modified by tsaiwn@cs.nctu.edu.tw
# you can get from here:  https://goo.gl/6jtP41   ; Search dummy + iottalk  for other files
import time, DAN, requests, random 
import threading, sys # for using a Thread to read keyboard INPUT
from tkinter import *  # 注意是 tkinter (Python 3.x); 不是 Tkinter (Python 2.x) 喔

#  注意你用的 IoTtalk 伺服器網址或 IP 
# ServerURL = 'http://192.168.33.88:9999' #with no secure connection
ServerURL = 'https://7.iottalk.tw' # with SSL secure connection
myName = "SYC_D."+ str( random.randint(600,999 ) ) 

tk = Tk()
tk.title("087_SYC Tk_Slider_請注意 Tk 必須當老大要在 main thread")
text_widget = Text(tk, height=2, width=36, font=("Simsun", 24), fg="red", bg="lightgreen"); 
text_widget.pack( ); 
text_widget.insert(END, "拉到滿意的值然後放掉滑鼠!")

gotSlider=False
sliderVal = 58  #initVal for the Slider
firstSetSlider=True  # 在一開始 .set(58) 設定 Slider故意不處理 # 已改用滑鼠放掉, 此變數沒用了
def syy_changed(event): 
    global gotSlider, sliderVal  #用來和原先的老大溝通 
    sliderVal=s.get()
    gotSlider=True

s = Scale(tk, from_=0, to=100, length=600, tickinterval=10, bg="lightyellow", fg="red",
    orient=HORIZONTAL)    #:# orient=HORIZONTAL, command=syy_changed)
# Connect the slider to the callback function
s.bind("<ButtonRelease-1>", syy_changed)  # 滑鼠放掉才算
s.set(sliderVal); s.pack()  # 如果 command 寫在 Scale( ... 那句, 則這 s.set( ) 也會執行它

def kill_me():
    global allDead  # 用來通知 thread 自殺
    allDead=True  #通知所有 thread 自殺
    tk.focus_set()
    sayBye( )
    tk.quit()  # close Tk window

button = Button(tk, text="Quit 點這結束程式", anchor="w",
  bg="yellow", fg="green", command=kill_me)
button.pack(side='right')
tk.protocol("WM_DELETE_WINDOW", kill_me)

Reg_addr = None #if None, Reg_addr = MAC address #(本來在 DAN.py 要這樣做 :-) 
# Note that Reg_addr 在以下三句會被換掉! # the mac_addr in DAN.py is NOT used
mac_addr = 'C9870D238' + str( random.randint(100,999 ) )  # put here for easy to modify :-)
# 若希望每次執行這程式都被認為同一個 Dummy_Device, 要把上列 mac_addr 寫死, 不要用亂數。
Reg_addr = mac_addr   # Note that the mac_addr generated in DAN.py always be the same cause using UUID !

DAN.profile['dm_name']='Dummy_Device'   # you can change this but should also add the DM in server
DAN.profile['df_list']=['Dummy_Sensor', 'Dummy_Control']   # Check IoTtalk to see what IDF/ODF the DM has
def initIoTtalk( ):
   ServerURL = 'https://7.iottalk.tw'
   DAN.profile['dm_name']='Syc_Dummy_087'
   DAN.profile['df_list']=['Color-I', 
                           'Slider', 
                           'Dmy_s087', 
                           'Dummy_Control']
   DAN.profile['d_name']= 'Syc_Dummy_087' + '_' + str( random.randint(100,999 ) )
   DAN.device_registration_with_retry(ServerURL, Reg_addr) 
   print("dm_name is ", DAN.profile['dm_name']) ; print("Server is ", ServerURL)
##
theInput="haha"
gotInput = allDead = False
firstRead=True
def doRead( ):
   global gotInput, theInput, allDead, firstRead
   while True:
      if(allDead):
         break
      if gotInput:
         time.sleep(0.1)
         continue  # go back to while
      try:
         if firstRead:
            print("提醒輸入 quit 會結束 !")  #只在第一次輸入之前才提醒
            firstRead=False
         theInput = input("Give me data: ")
         
      ######################################
         args = theInput.split(' ')
         if args[0] == "l":
            if len(args) != 2:
               print("wrong input for lumin")
               continue
            DAN.push("Slider", max(min(int(args[1]), 99), 0))
            
         elif args[0] == "c":
            if len(args) != 4:
               print("wrong input for color")
               continue
            color1 = min(max(int(args[1]), 0), 255)
            color2 = min(max(int(args[2]), 0), 255)
            color3 = min(max(int(args[3]), 0), 255)
            
            DAN.push("Color-I", color1, color2, color3)
      #######################################  
             
      except KeyboardInterrupt:
         allDead = True
         break
      except Exception:    ##  KeyboardInterrupt:
         allDead = True
         sys.stdout = sys.__stdout__
         print(" Thread say Bye bye ---------------", flush=True)
         break  # raise   #  sys.exit(0);   ## break  # raise   #  ?
      gotInput=True
      if(allDead): kill_me( )
      elif theInput !='quit' and theInput != "exit":
         print("Will send " + theInput, end="   , ")

#creat a thread to do Input data from keyboard, by tsaiwn@cs.nctu.edu.tw
threadx = threading.Thread(target=doRead)
threadx.daemon = True

def doDummy( ):  # 因為 Tkinter  必須在 main thread, 所以原先的主程式必須改用 thread (thready)
  global gotInput, theInput, allDead  # do NOT forget these var should be global
  global gotSlider, firstSetSlider  # 沒寫  sliderVal = xxx 就不必寫 global 
  while True:
    if(allDead): break
    try:
    #Pull data from a device feature called "Dummy_Control"
        value1=DAN.pull('Dummy_Control')
        if value1 != None:
            print (value1[0])
    #Push data to a device feature called "Dummy_Sensor" 
        if gotSlider:  # Slider 有被動到
           sss = sliderVal  # 取出 slider value
           gotSlider = False #其實沒用處, 因為我們不管 user 是否會去改變  Slider
           
           #######################
           DAN.push("Slider", sss)
           #######################
           
         #   if firstSetSlider:
         #      firstSetSlider=False
         #      DAN.push ('Dummy_Sensor', 100);  time.sleep(0.2)  # 怕燈泡來不及收取
         #      DAN.push ('Dummy_Sensor', 0);  time.sleep(0.2) # 這時 DAI6.py 收不到這兩個喔 ! 想想why?
         #      print ("Slider 第一次的值: ", sss)  # 可在第一次故意先送 100, 再送 0, 再送 sss
         #      DAN.push ('Dummy_Sensor', sss)  # 若不送就把這列註解掉
         #      pass    # 第一次是我們 .set( ) 的, 故意不處理; # 現改check滑鼠放掉不會查到  .set(58)
         #   else:  # 不是我們一開始 .set( )的 !
         #      print ("Slider 被拉到 ", sss)  # 可以用  DAN.push( ) 送去 IoTtalk server
         #      DAN.push ('Dummy_Sensor', sss)
        #end of if gotSlider
        if gotInput:
           if theInput =='quit' or theInput=="exit":
              allDead = True
              break;  #  sys.exit( );
           #value2=random.uniform(1, 10)
         #   try:
         #      value2=float( theInput )
         #   except:
         #      value2=0
           gotInput=False   # so that you can input again 
           if(allDead): break;
         #   DAN.push ('Dummy_Sensor', value2,  value2)  #  故意多送一個 
        #end of if gotInput
    except KeyboardInterrupt:
        allDead = True
        break;  # sys.exit( );
    except Exception as e:
        print("allDead: ", allDead)
        if(allDead):
            break  #  do NOT try to re-register !
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr IS not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)    
    if(allDead): break
    try:
       time.sleep(0.1)  # was 0.2
    except KeyboardInterrupt:
       break
  print("=== end of thready")
  time.sleep(0.015)
  kill_me( );
  sys.exit(0);

def sayBye( ):   # 用來向 IoTtalk 解除註冊 Deregister
  try: 
     time.sleep(0.025)
     DAN.deregister()
  except Exception as e:
     print("===De-Reg Error")
  print("Bye ! --------------", flush=True)
  # sys.exit(0);

# 以下三列把 doDummy 包成 thready 然後叫它平行啟動
thready = threading.Thread(target=doDummy)
thready.daemon = True

if __name__ == '__main__':
   initIoTtalk( )
   threadx.start()
   thready.start()
   tk.mainloop()  #  tk GUI 必須當老大, 在 main thread