import time
import numpy

import pypot.dynamixel

ports = pypot.dynamixel.get_available_ports()
if not ports:
    exit('No port')

dxl_io = pypot.dynamixel.DxlIO(ports[0]) #Gather the USB port with Dynamixel mootors connect to

#dxl_io.factory_reset()
dxl_io.set_wheel_mode([1, 2]) #Set the motor with id 1 and 2 to wheel mode

dxl_io.set_moving_speed({1: 50}) #Set the motor 1 to speed 50*1.339 rpm
dxl_io.set_moving_speed({2: 90}) #Set the motor 2 to speed 90*1.339 rpm
time.sleep(5) #wait 5 seconds
dxl_io.set_moving_speed({1: 0}) #Stop both robots
dxl_io.set_moving_speed({2: 0})
