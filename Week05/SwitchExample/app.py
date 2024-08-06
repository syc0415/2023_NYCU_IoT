from flask import Flask, request, abort
from flask import render_template
from flask import make_response

import csmapi

app = Flask(__name__)

@app.route('/<device_id>/', methods=['GET'])
def remote_control(device_id):
    try:    
        profile = csmapi.pull(device_id, 'profile')

        if profile:
            Ctl_O = csmapi.pull(device_id, '__Ctl_O__')
            if Ctl_O != []:
                selected_df_flags = Ctl_O[0][1][1]['cmd_params'][0]
                df_list = profile['df_list']
                df_dict = {'Butt': 0, 'Colo': 0, 'Keyp': 0, 'Knob': 0, 'Swit': 0, 'Togg':0, 'Slid':0}
                for index, element in list(enumerate(selected_df_flags)):
                    if element == '1': 
                        df_dict[df_list[index][:4]] += 1
            return make_response(render_template('switch.html', device_id=device_id, df_dict=df_dict))        
        # print(df_dict)
        
    except Exception as e:    
        # print('Error: {}'.format(e))
        return 1

@app.route('/<device_id>/<count>/', methods=['GET'])
def switch_generator(device_id, count):

    sync = request.args.get('sync')
    if sync != 'True': sync = False

    def register_remote_control(device_id):
        profile = {
            'd_name': device_id,
            'dm_name': 'Remote_control',
            'u_name': 'yb',
            'is_sim': False,
            'df_list': [],
        }
        for i in range(1,26):
            profile['df_list'].append("Switch%d" % i)
            
        try:
            result = csmapi.register(device_id, profile)
            if result: print('Remote control generator: Remote Control successfully registered.')
            return result
        except Exception as e:
            print('Remote control generator: ', e)

    profile = None
    try:
        profile = csmapi.pull(device_id, 'profile')
    except Exception as e:
        print('Remote control generator: ', e)
        if str(e).find('mac_addr not found:') != -1:
            print('Remote control generator: Register Remote Control...')
            result = register_remote_control(device_id)
            return 'Remote control "'+device_id+'" successfully registered. <br> Please bind it in the IoTtalk GUI.', 200
        else:
            print('Remote control generator: I dont know how to handel this error. Sorry...pass.')
            abort(404)

    df_dict = {'Swit': 0}        
    df_dict['Swit']= int(count)
    return make_response(render_template('switch.html', device_id=device_id, df_dict=df_dict, sync=sync))        

if __name__ == "__main__":
    app.run('0.0.0.0', port=32767, threaded=True, use_reloader=False)