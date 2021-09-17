

"""
Control Loops
Number	Name	xml Tag	    Units	xml Tag	    Operating Range	xml Tags	Sensor Range	xml Tags	                    Description / Notes
1	    TEMP	AI_Name_1	°C	    SYS_Units	4-44°C	        SP_1, PV_1	0-50°C	        CLC_SP_Low_1, CLC_SP_High_1	    Dedicated, primary, temperature control loop for chamber temperature, PID control, Heat/Cool.
2	    %RH	    AI_Name_2	%RH	    AI_Units_2	0-99%RH	        SP_2, PV_2	0-100%RH	    CLC_SP_Low_2, CLC_SP_High_2	    Relative humidity control loop inside chamber, PID control, additive humidification and dehumidification
3	    CO2	    AI_Name_3	PPM	    AI_Units_3	0-5,000PPM	    SP_3, PV_3	0-5,000PPM	    CLC_SP_Low_3, CLC_SP_High_3	    CO2 control loop inside chamber, PID control, additive CO2 and CO2 scrubbing
4	    LS4	    AI_Name_4	UML	    AI_Units_4	0-1,500UML	    SP_4, PV_4	0-1,500UML	    CLC_SP_Low_4, CLC_SP_High_4	    PAR light sensor, no control loop, monitoring of process value only, can be configurde for closed-loop control
5	    WVC5	AI_Name_5	%WC	    AI_Units_5	0-100%WC	    SP_5, PV_5	0-100%WC	    CLC_SP_Low_5, CLC_SP_High_5	    Irrigation control loop, PID, additive watering only to achieve % volumetric water content SP only
6	    *unused*	AI_Name_6		AI_Units_6		            SP_6, PV_6		            CLC_SP_Low_6, CLC_SP_High_6	    Unused control slot, universal input with 2 channel PID output loops, possible 2nd irrigation zone, or other
7	    VEST	AI_Name_7	°C	    AI_Units_7	4-44°C	        SP_7, PV_7	0-50°C	        CLC_SP_Low_7, CLC_SP_High_7	    Temperature sensor in vestibule, monitoring only

"""

"""

    To read:
    
    Temperature = PV_1
    Relative Humidity = PV_2
    CO2 = PV_3
    Light Sensor = PV_4
    Watering = PV_5
    
    To Write:
    
    Temperature = CM_SP_1_Manual
    RH = CM_SP_2_Manual
    CO2 = CM_SP_3_Manual
    Light Sensor = read only
    Watering = CM_SP_5_Manual

"""

import requests
from collections import OrderedDict
from lxml import etree
from datetime import datetime
"""

tag_map = {
    'EO_1_On_Off': False, 'EO_1_Dim': 0, 'EO_2_On_Off': False, 'EO_2_Dim': 0

}





def get_base_url(chamber_id):

    return 'http://env-gc-{}.agron.iastate.edu/read_data.xml'.format(chamber_id)



def get_chamber_values(chamber_id, tags):

    payload = {
        'Cmd': 'read',
        'Tag': tags
    }

    r = requests.get(
        get_base_url(chamber_id),
        params=payload
    )

    return parse_percival_response(r.text)



def get_relative_humidity(chamber_id):
    ## gets the relative humidity state for a chamber
    #tags = ['SP_2', 'PV_2', 'AI_Name_2']
    tags = ['PV_2']

    return get_chamber_values(chamber_id, tags)



def get_lights(chamber_id):
    ## gets the current lighting state for a chamber

    tags = ['EO_1_On_Off', 'EO_2_On_Off', 'EO_1_Dim', 'EO_2_Dim']
    return get_chamber_values(chamber_id, tags)


    payload = {
        'Cmd': 'read',
    }

    r = requests.get(
        get_base_url(chamber_id),
        params=payload
    )

    return parse_percival_response(r.text)



def parse_percival_response(resp_str):
    resp_dict = {}
    r_xml = etree.fromstring(resp_str)
    context = etree.iterwalk(r_xml, events=("start",))

    for action, elem in context:

        if elem.tag == 'Req':
            continue

        if elem.tag.endswith('_Dim'):
            val = int(elem.text.rstrip(" %"))

        elif elem.tag.endswith('_On_Off'):

            if elem.text == 'On':
                val = True
            else:
                val = False
        else:
            val = elem.text

        resp_dict[tag_mapper(elem.tag)] = val

    return resp_dict



def set_temperature(chamber_id, temp):

    level_multiplier = 1000
    payload = {
        'Cmd': 'write',
        'CM_SP_1_Manual': temp * level_multiplier
    }

    r = requests.get(
        get_base_url(chamber_id)
        , params=payload
    )

    return parse_percival_response(r.text)



def set_relative_humdity(chamber_id, level):
    level_multiplier = 10000
    payload = {
        'Cmd': 'write',
        'CM_SP_2_Manual': level * level_multiplier
    }


    r = requests.get(
        get_base_url(chamber_id)
        , params=payload
    )

    return parse_percival_response(r.text)


def set_lights(chamber, level):
    # level is a float between 0 and 1 inclusive
    # The chamber controller expects input values of percent*1000. For example, 20% should be input as 20000
    #
    level_multiplier = 10000

    # Build a dictionary of querystring key/value pairs:
    params_dict = OrderedDict()
    params_dict['Cmd'] = 'write'

    if level == 0:
        on_off = 'Off'
    else:
        on_off = 'On'

    new_level = round(level*level_multiplier)

    for i in range(1, 3):

        params_dict["EO_{}_On_Off".format(i)] = on_off
        params_dict["EO_{}_Dim".format(i)] = new_level


    r = requests.get(
        get_base_url(chamber)
        , params=params_dict
    )

    return parse_percival_response(r.text)





# A dictionary mapping human-readable variable names to chamber control tag names:
tags = {}

#print(get_lights(8))

def tag_mapper(tag_str):

    if tag_str in ['EO_1_On_Off', 'EO_1_Dim', 'EO_2_On_Off', 'EO_2_Dim']:
        return tag_str.replace('EO', 'Lighting').replace('_Off', '').lower()

    if tag_str in ['SP_2', 'PV_2']:

        if tag_str == 'SP_2':
            return 'humidity_1'
        elif tag_str == 'PV_2':
            return 'humidity_2'





    return tag_str
"""



class GrowthChamberControl:
    TIMEOUT = 3.0
    SUPERVISOR_RPC_URL = 'http://localhost:9001/RPC2'
    __level_multiplier = 1000

    __growth_chamber_base_url = 'http://env-gc-{}.agron.iastate.edu/read_data.xml'

    __tag_map = {
        # SENSOR READINGS:
       'PV_1': 'temperature_actual'
        , 'PV_2': 'humidity_actual'
        , 'PV_3': 'co2_actual'
        , 'PV_4': 'lighting_sensor'
        , 'PV_5': 'watering_actual'
        # WRITE COMMAND TAGS:
        , 'CM_SP_1_Manual': 'temperature_target'
        , 'CM_SP_2_Manual': 'humidity_target'
        , 'CM_SP_3_Manual': 'co2_target'
        ,'CM_SP_5_Manual': 'watering_target'
        # LIGHTING SPECIFIC WRITE COMMANDS:
        , 'EO_1_On_Off': 'lighting_1_on'
        , 'EO_2_On_Off': 'lighting_2_on'
        , 'EO_1_Dim': 'lighting_1'
        , 'EO_2_Dim': 'lighting_2'
        , 'EO_3_Dim': 'lighting_3'
        , 'EO_4_Dim': 'lighting_4'
        , 'EO_5_Dim': 'lighting_5'
        , 'EO_6_Dim': 'lighting_6'
        , 'EO_7_Dim': 'lighting_7'
        , 'PV_4': 'light_meter'

        # Humidity enable/disable:
        , 'CLC_Enable_Rh_1': 'humidification_enabled'
        , 'CLC_Enable_Rh_2': 'dehumidification_enabled'

        # DOOR, ETC:
        , 'EO_13_On_Off': 'door_state'
        #, 'EO_16_On_Off': 'door_state'
        , 'EO_14_On_Off': 'air_diverter_state'
        #, 'EO_17_On_Off': 'air_diverter_state'
        , 'EO_15_On_Off': 'curtain_state'
        #, 'EO_18_On_Off': 'curtain_state'
        # CHAMBER MODE:
        , 'CM_NON_RAMPING_MODE': 'operating_mode'

        # Clock:
        , 'Real_Time_Hour': 'hour'
        , 'Real_Time_Minute': 'minute'
        , 'Real_Time_Second': 'second'



    }

    # The reverse of the above key=>value mapping:
    __rev_tag_map = {v:k for k,v in __tag_map.items()}


    def __init__(self, chamber_id):

        self.chamber_id = chamber_id


    def __tag_mapper(self, tag_str):

        if tag_str in self.__tag_map.keys():
           return self.__tag_map[tag_str]
        else:
            return None


    def __get_base_url(self):
        return self.__growth_chamber_base_url.format(self.chamber_id)


    def __parse_percival_response(self, resp_str):

        resp_dict = {}
        r_xml = etree.fromstring(resp_str)
        context = etree.iterwalk(r_xml, events=("start",))


        for action, elem in context:

            if elem.tag == 'Req':
                continue

            if elem.tag.endswith('_Dim'):
                val = int(elem.text.rstrip(" %"))

            elif elem.tag.endswith('_On_Off'):

                if elem.text == 'On':
                    val = True
                else:
                    val = False

            else:

                try:

                    val = float(elem.text.split(" ")[0])
                except ValueError:

                    if elem.text == 'No':
                        val = False
                    elif elem.text == 'Yes':
                        val = True
                    else:
                        val = elem.text

            '''
            print(elem)
            print(elem.tag)
            print(elem.text)
            print(val)
            print("-----------------------")
            '''
            resp_dict[self.__tag_mapper(elem.tag)] = val

            # We are adding the chamber ID to the response from the chamber so that we have access to it
            # in the django_celery_results app which does not store args or kwargs, only response vals:
            resp_dict['chamber_id'] = self.chamber_id

            try:
                resp_dict['env_var'] = self.__tag_mapper(elem.tag).split("_")[0]
            except AttributeError:

                print(elem)
                print(elem.tag)


            resp_dict['env_val'] = val

        return resp_dict


    '''
    def __parse_percival_response(self, resp_str):
        resp_dict = {}
        r_xml = etree.fromstring(resp_str)
        context = etree.iterwalk(r_xml, events=("start",))


        for action, elem in context:

            if elem.tag == 'Req':
                continue

            if elem.tag.endswith('_Dim'):
                val = int(elem.text.rstrip(" %"))

            elif elem.tag.endswith('_On_Off'):

                if elem.text == 'On':
                    val = True
                else:
                    val = False

            else:
                val = float(elem.text.split(" ")[0])

            resp_dict[self.__tag_mapper(elem.tag)] = val

            # We are adding the chamber ID to the response from the chamber so that we have access to it
            # in the django_celery_results app which does not store args or kwargs, only response vals:
            resp_dict['chamber_id'] = self.chamber_id
            resp_dict['env_var'] = self.__tag_mapper(elem.tag).split("_")[0]
            resp_dict['env_val'] = val

        return resp_dict
    '''


    def __make_set_request(self, tags_dict):


        # Attempt to translate from our local param names to the Percival tag names:
        tags_dict = {self.__rev_tag_map.get(k, k):v for k,v in tags_dict.items()}

        # We need the querystring params to be in a certain order, starting with 'Cmd',
        # so add the incoming tags to an ordered dict:
        payload = OrderedDict()
        payload['Cmd'] = 'write'
        # Merge the incoming tags dictionary:
        payload.update(tags_dict)

        #print('WHAT IS PAYLOAD?')
        #print(payload)
        #print("----------------")

        r = requests.get(
            self.__get_base_url()
            , params=payload
        )

        #print('WHAT IS RESPONSE TEXT?')
        #print(r.text)

        return self.__parse_percival_response(r.text)


    def __get_chamber_values(self, tags_list):

        payload = {
            'Cmd': 'read',
            'Tag': [self.__rev_tag_map.get(tag) for tag in tags_list]
        }

        try:
            r = requests.get(
                self.__get_base_url(),
                params=payload,
                timeout=self.TIMEOUT
            )

            return self.__parse_percival_response(r.text)
        except requests.exceptions.ConnectTimeout:
            return {"type": "ConnectionError"}


    # DOOR, SHADE, ETC:

    def open_door(self):
        payload = {
            #'EO_16_On_Off': 'On'
            'EO_13_On_Off': 'On'
        }
        return self.__make_set_request(payload)


    def close_door(self):
        payload = {
            #'EO_16_On_Off': 'Off'
            'EO_13_On_Off': 'Off'
        }
        return self.__make_set_request(payload)


    def get_door(self):
        tags = ['door_state']
        return self.__get_chamber_values(tags)


    def open_curtain(self):
        payload = {
            'EO_15_On_Off': 'On'
        }
        return self.__make_set_request(payload)

    def close_curtain(self):
        payload = {
            'EO_15_On_Off': 'Off'
        }
        return self.__make_set_request(payload)

    def get_curtain(self):
        tags = ['curtain_state']
        return self.__get_chamber_values(tags)

    def turn_on_air_diverter(self):
        payload = {
            'EO_14_On_Off': 'On'
        }
        return self.__make_set_request(payload)

    def turn_off_air_diverter(self):
        payload = {
            'EO_14_On_Off': 'Off'
        }
        return self.__make_set_request(payload)

    def get_air_diverter(self):
        tags = ['air_diverter_state']
        return self.__get_chamber_values(tags)

    # LIGHTING

    def set_lighting(self, level):

        # level is a float between 0 and 1 inclusive
        # The chamber controller expects input values of percent*1000. For example, 20% should be input as 20000
        #

        __level_multiplier = 1000 #0

        # Build a dictionary of querystring key/value pairs:

        if level == 0:
            on_off = 'Off'
        else:
            on_off = 'On'

        new_level = round(level * __level_multiplier)

        tags = {
            #'lighting_1_on': on_off
            #, 'lighting_2_on': on_off
            'lighting_1': new_level
            , 'lighting_2': new_level
            , 'lighting_3': new_level
            , 'lighting_4': new_level
            , 'lighting_5': new_level
            , 'lighting_6': new_level
            , 'lighting_7': new_level
        }

        #for i in range(1, 3):
        #    tags["EO_{}_On_Off".format(i)] = on_off
        #    tags["EO_{}_Dim".format(i)] = new_level

        return self.__make_set_request(tags)


    def get_lighting(self):
        ## gets the current lighting state for a chamber
        #tags = ['lighting_1_on', 'lighting_1', 'lighting_2_on', 'lighting_2']
        tags = ['lighting_' + str(i) for i in range(1,8)]
        #tags.append("SP_4")
        tags.append("light_meter")
        return self.__get_chamber_values(tags)


    # RELATIVE HUMIDITY

    def set_humidity(self, level):

        payload = {
            'CM_SP_2_Manual': level * self.__level_multiplier
        }

        return self.__make_set_request(payload)


    def get_humidity(self):
        ## gets the relative humidity state for a chamber
        tags = ['humidity_actual', 'humidity_target', 'humidification_enabled', 'dehumidification_enabled']

        return self.__get_chamber_values(tags)


    def disable_humidity(self):
        ''' Disables humidification in a chamber. This is useful when you don't want to spray a robot with water.'''

        payload = {
            #'ENS_Hum_Enable_Source': 'Off'
            'CLC_Enable_Rh_1': 'No', # humidification
            'CLC_Enable_Rh_2': 'No', # dehumidification
        }
        return self.__make_set_request(payload)


    def enable_humidity(self):
        ''' Enables humidity control via the api. '''

        payload = {
            'CLC_Enable_Rh_1': 'Yes', # humidification
            'CLC_Enable_Rh_2': 'Yes', # dehumidification
        }
        new_state = self.__make_set_request(payload)
        return self.get_humidity()


    def disable_temperature(self):
        ''' Idea is to stop temperature controls to quiet the air movement within the chamber
        so that accurate measurements can be taken without leaf movement... '''

        # First, get the current temp:

        # We need to disable the relevant Celery worker/queue:

        # Pass the current temp as the set-point:


    # TEMPERATURE
    def set_temperature(self, temperature):
        payload = {
            'temperature_target': temperature * self.__level_multiplier
        }
        return self.__make_set_request(payload)

    def get_temperature(self):
        #tags = ['PV_1', 'CM_SP_1_Manual']
        tags = ['temperature_actual', 'temperature_target']

        return self.__get_chamber_values(tags)



    # CO2

    def set_co2(self, level):
        payload = {
            'CM_SP_3_Manual': level * self.__level_multiplier
        }
        return self.__make_set_request(payload)


    def get_co2(self):
        tags = ['co2_actual', 'co2_target']
        return self.__get_chamber_values(tags)


    # WATERING:
    def set_watering(self, level):

        payload = {
            'CM_SP_5_Manual': level * self.__level_multiplier
        }
        return self.__make_set_request(payload)


    def get_watering(self):
        tags = ['watering_actual', 'watering_target']

        return self.__get_chamber_values(tags)


    def get_state(self):
        tags = [
            'co2_actual', 'co2_target', 'co2_actual', 'co2_target', 'humidity_actual', 'humidity_target',
            'humidification_enabled', 'dehumidification_enabled',
            #'lighting_1_on', 'lighting_1', 'lighting_2_on', 'lighting_2',
            'lighting_1', 'lighting_2', 'lighting_3', 'lighting_4', 'lighting_5', 'lighting_6', 'lighting_7'
            , 'temperature_actual', 'temperature_target'
            , 'air_diverter_state', 'watering_actual', 'watering_target'
            , 'door_state', 'curtain_state', 'operating_mode',
        ]

        return self.__get_chamber_values(tags)


    def get_time(self):
        ret_val = self.__get_chamber_values(["hour", "minute", "second"])
        # Some housekeeping:
        del ret_val["env_var"]
        del ret_val["env_val"]
        # No need for floats for the time values:
        for k in ret_val:
            ret_val[k] = int(ret_val[k])

        return ret_val


    def set_time(self):
        now = datetime.now()

        payload = {
            'Real_Time_Hour': now.hour
            , 'Real_Time_Minute': now.minute
            , 'Real_Time_Second': now.second
        }
        return self.__make_set_request(payload)


    def get_mode(self):
        ''' Returns the current operational mode of the chamber (manual, diurnal, etc).'''
        return self.__get_chamber_values(['operating_mode'])


    def set_mode(self, new_mode):
        ''' Changes the chamber's current operating mode '''

        mode_str = new_mode

        payload = {
            # 'CM_NON_RAMPING_MODE': new_mode
            'Cmd': 'run',
            'Item': mode_str
        }

        '''
        nr_manual and/or ramping_manual Manual – controller is holding constant set points, controlled manually
        nr_diurnal Diurnal – The 2 step, simple program
        ramping_daily_light_integral DLI – This is another simple, 2 step program like diurnal
        Program – The controller is running a single multi-step program
        Sequence – The controller is running a sequence of programs

        Manual, Non-Ramping 
        ramping.xml?Cmd=run&Item=nr_manual
        Ramping Manual Programming (Default State)
        ramping.xml?Cmd=run&Item=ramping_manual
        Diurnal Programming
        ramping.xml?Cmd=run&Item=nr_diurnal
        DLI Programming
        ramping.xml?Cmd=run&Item=ramping_daily_light_integral
        '''

        ''' To set mode, we call a different url (ramping.xml vs read_data.xml), so we are not using
        self.__get_base_url() here '''

        r = requests.get(
            'http://env-gc-{}.agron.iastate.edu/ramping.xml'.format(self.chamber_id),
            params=payload,
            timeout=self.TIMEOUT
        )

        print("-------")
        print(payload)
        print(r.text)
        print("-------")

        return r.text

if __name__ == '__main__':
    import sys
    #print(tag_mapper('EO_1_Dim'))
    #set_lights(8, 0)
    #print(set_lights(8, 0))
    #set_lights(8, 1)

    CHAMBER_ID = 8

    for i in range(1,9):
        print(i)
        chamber = GrowthChamberControl(i)
        #print(chamber.set_time())
        print(chamber.get_time())

    sys.exit(0)

    print(chamber.open_door())

    from time import sleep
    sleep(5)

    print(chamber.get_door())
    print(chamber.get_curtain())
    print(chamber.get_air_diverter())

    print(chamber.close_door())

    sleep(4)
    print(chamber.get_door())

    sys.exit(0)

    NEW_TEMP = 22
    NEW_LIGHTING = 0


    print("TEMPERATURE:")
    print(chamber.get_temperature())
    print("LIGHTING:")
    print(chamber.get_lighting())
    print("HUMIDITY:")
    print(chamber.get_humidity())
    print("CO2:")
    print(chamber.get_co2())
    print("WATERING")
    print(chamber.get_watering())


    #chamber.set_temperature(NEW_TEMP)
    #chamber.set_lighting(NEW_LIGHTING)

    print("-" * 40)

    #print("TEMPERATURE:")
    #print(chamber.get_temperature())
    #print("LIGHTING:")
    #print(chamber.get_lighting())


    sys.exit(0)


    print("RELATIVE HUMIDITY:")
    print(chamber.get_relative_humidity())
    print("TEMPERATURE:")
    print(chamber.get_temperature())
    print("CO2:")
    print(chamber.get_co2())
    print("WATERING:")
    print(chamber.get_watering())
    print("LIGHTING:")
    print(chamber.get_lighting())


    #print(set_temperature(CHAMBER_ID, 15))

    """

    print(get_lights(CHAMBER_ID))
    print()

    #print(set_relative_humdity(8, 'RH'))

    print()
    print(get_relative_humidity(CHAMBER_ID))
    """

    #print(get_lights(8))
