import csmapi

csmapi.ENDPOINT = "https://7.iottalk.tw"
device_id = "109550087"

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
    print(df_dict)
    
except Exception as e:    
    print('Error: {}'.format(e))

