import random 
import time

ServerURL = 'https://7.iottalk.tw' #For example: 'https://iottalk.tw'
MQTT_broker = '7.iottalk.tw' # MQTT Broker address, for example:  'iottalk.tw' or None = no MQTT support
MQTT_port = 5566
MQTT_encryption = True
MQTT_User = 'iottalk'
MQTT_PW = 'iottalk2023'

device_model = 'Dummy_Device'
IDF_list = ['Dummy_Sensor']
ODF_list = ['Dummy_Control']
device_id = 'SYC_087' #if None, device_id = MAC address
device_name = 'SYC_087'
exec_interval = 0.1  # IDF/ODF interval

def on_register(r):
    print('Server: {}\nDevice name: {}\nRegister successfully.'.format(r['server'], r['d_name']))

late_data = []
def Dummy_Sensor():
    global send_data, start
    send_data = random.randint(0, 100)
    start = time.perf_counter()
    
    return send_data

def Dummy_Control(data:list):
    global send_data, start, late_data
    if data[0] == send_data:
        print('got', len(late_data), 'data')
        late_data.append(time.perf_counter() - start)
        if len(late_data) == 100:
            print('avg latency:', sum(late_data) / len(late_data))
    
