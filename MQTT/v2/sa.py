import random
import time

from iottalkpy.dan import NoData

### The registeration api url, you can use IP or Domain.
api_url = 'https://iottalk2.tw/csm'  # default
# api_url = 'http://localhost/csm'  # with URL prefix
# api_url = 'http://localhost:9992/csm'  # with URL prefix + port

### [OPTIONAL] If not given or None, server will auto-generate.
# device_name = 'Dummy_Test'

### [OPTIONAL] If not given or None, DAN will register using a random UUID.
### Or you can use following code to use MAC address for device_addr.
# from uuid import getnode
# device_addr = "{:012X}".format(getnode())
# device_addr = "..."

### [OPTIONAL] If the device_addr is set as a fixed value, user can enable
### this option and make the DA register/deregister without rebinding on GUI
# persistent_binding = True

### [OPTIONAL] If not given or None, this device will be used by anyone.
# username = 'myname'

### The Device Model in IoTtalk, please check IoTtalk document.
device_model = 'Dummy_Device'

### The input/output device features, please check IoTtalk document.
idf_list = ['DummySensor-I']
odf_list = ['DummyControl-O']

### Set the push interval, default = 1 (sec)
### Or you can set to 0, and control in your feature input function.
push_interval = 0.1  # global interval
interval = {
    'Dummy_Sensor': 3,  # assign feature interval
}


def on_register(dan):
    print('register successfully')


late_data = []
def DummySensor_I():
    global send_data, start
    send_data = random.randint(0, 100)
    start = time.perf_counter()
    
    return send_data


def DummyControl_O(data: list):
    global send_data, start, late_data
    if data[0] == send_data:
        print('got', len(late_data), 'data')
        late_data.append(time.perf_counter() - start)
        if len(late_data) == 100:
            print('avg latency:', sum(late_data) / len(late_data))
