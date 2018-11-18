"""This module is main module for contestant's solution."""

from hackathon.utils.control import Control
from hackathon.utils.utils import ResultsMessage, DataMessage, PVMode, \
    TYPHOON_DIR, config_outs 
from hackathon.framework.http_server import prepare_dot_dir


def worker(msg: DataMessage) -> ResultsMessage:
    """TODO: This function should be implemented by contestants."""
    # Details about DataMessage and ResultsMessage objects can be found in /utils/utils.py

    battery = msg.bessSOC * 100 
    load_one = True
    load_two = True
    load_three = True
    power_reference = 0.0
    pv_mode = PVMode.ON
#2087.19 $
#grid active

    if msg.grid_status:
        #puni se sa jeftinom strujom
        if battery < 99 and msg.buying_price < 5:
            power_reference = - 5.0
        #ako ima viska solarne energije, baterija se puni
        if msg.buying_price < 5:
            if(msg.solar_production >= msg.current_load):
                power_reference = -(msg.solar_production-msg.current_load)
            #ako ima premalo solarne, aktivira se baterija da pomaze
            if(msg.solar_production < msg.current_load):
                if (msg.current_load-msg.solar_production)<=5.0:
                    power_reference  = (msg.current_load - msg.solar_production)
                else:
                    power_reference = 0.0

        if battery < 99 and msg.buying_price < 5:
            power_reference = - 5.0
        #koliki je minimum baterije
        if battery < 25:
            power_reference = 0.0
        
        #ukoliko je skupa struja sta radimo
        if msg.buying_price > 5:
            if(msg.solar_production >= msg.current_load):
                power_reference = -(msg.solar_production-msg.current_load)
            #ako ima premalo solarne, aktivira se baterija da pomaze
            if(msg.solar_production < msg.current_load):
            	if battery >= 10:
            		if (msg.current_load-msg.solar_production)<=5.0:
            			power_reference = (msg.current_load - msg.solar_production)
            		else:
            			power_reference = +5.0
        if battery < 99 and msg.buying_price < 5:
            power_reference = - 5.0



        




        '''
        if battery >10 and msg.buying_price ==8:
            power_reference = +5.0
        pv_mode = PVMode.ON
        if msg.solar_production > 0:
            if msg.solar_production > msg.current_load and msg.buying_price == 3:
                power_reference = -5.0
            elif msg.solar_production > msg.current_load:
                power_reference = -(msg.solar_production - msg.current_load)
            else:
                if battery < 80 and msg.buying_price == 3:
                    power_reference = -5.0
                elif battery < 10:
                    power_reference = 0.0
                else:
                    if msg.current_load <= 5.0:
                        power_reference = msg.current_load
                    else:
                        power_reference = +5.0

        else:
            if msg.buying_price == 8:
                if battery > 10:
                    power_reference = +3.5
                else:
                    power_reference = 0.0
            else:
                if battery < 100:
                    power_reference = -4.99
                else:
                    power_reference = 0.0
        '''



    
#blackout
    else:
        if msg.solar_production > 0:
            if msg.solar_production == msg.current_load:
                power_reference = 0.0
            elif msg.solar_production > msg.current_load:
                if msg.solar_production - msg.current_load > 5:
                    pv_mode = PVMode.OFF
                    if msg.current_load > 5:
                        load_three = False
                        if msg.current_load > 5:
                            load_two = False
                    else:
                        power_reference = msg.current_load
            else:
                if msg.current_load - msg.solar_production > 5.0:
                    load_three = False
                    if msg.current_load - msg.solar_production > 5.0:
                        load_two = False
                    power_reference = msg.current_load 
                else:
                    power_reference = msg.current_load
                    

        else:
            load_three = False
            if msg.current_load <= 5.0:
                power_reference = msg.current_load
            else:
                load_two = False
                power_reference = msg.current_load


                    



        

    return ResultsMessage(data_msg=msg,
                          load_one=load_one,
                          load_two=load_two,
                          load_three=load_three,
                          power_reference=power_reference,
                          pv_mode=pv_mode)


def run(args) -> None:
    prepare_dot_dir()
    config_outs(args, 'solution')

    cntrl = Control()

    for data in cntrl.get_data():
        cntrl.push_results(worker(data))
