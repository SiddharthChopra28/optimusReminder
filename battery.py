#!/bin/python

from power import PowerManagement, POWER_TYPE_AC, POWER_TYPE_BATTERY #type:ignore
import time
from easygui import boolbox #type:ignore
import os
import subprocess
import sys

DATA_DIR = os.path.expanduser('~/.config/optimusReminder/')
FILENAME = 'battery_status.txt'
pluggedIn = None

time.sleep(5)

def get_curr_gpu():
    try:
        curr_status = subprocess.run(['optimus-manager', '--status'], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        return 'ERROR'
    else:
        gpu = curr_status.stdout.decode("utf-8").split('\n')[2].split(':')[1].strip()
        
    return gpu



try:
    battery = PowerManagement()
    
    if battery.get_providing_power_source_type() == POWER_TYPE_AC:
        pluggedIn = 1
    elif battery.get_providing_power_source_type() == POWER_TYPE_BATTERY:
        pluggedIn = 0
    
except Exception as e:
    print(e)
    sys.exit()
    

try:

    if not os.path.isdir(DATA_DIR):
        os.mkdir(DATA_DIR)
        
        file = open(os.path.join(DATA_DIR, FILENAME), 'w')
        file.write(str(pluggedIn))
        file.close()
   
except Exception as e:
    print(e)
    sys.exit()

gpu = get_curr_gpu()
if gpu != 'ERROR':
    

    if gpu == 'nvidia':
        if pluggedIn != 1:
                switch = boolbox('You are no longer plugged in. Would you like to switch to intel GPU?', 'Optimus Reminder', ['Do it automatically (Logout)', 'Do it manually'])
                
                if switch:
                    os.system('optimus-manager --switch nvidia --no-confirm')
                    
    elif gpu == 'intel':
        if pluggedIn != 0:
                switch = boolbox('You are now plugged in. Would you like to switch to nvidia GPU?', 'Optimus Reminder', ['Do it automatically (Logout)', 'Do it manually'])
                
                if switch:
                    os.system('optimus-manager --switch nvidia --no-confirm')



while True:
    battery = PowerManagement()
    
    file = open(os.path.join(DATA_DIR, FILENAME), 'r')
    status = int(file.read())
    file.close()

    
    if battery.get_providing_power_source_type() == POWER_TYPE_AC:
        pluggedIn = 1
    elif battery.get_providing_power_source_type() == POWER_TYPE_BATTERY:
        pluggedIn = 0
        
        
    if pluggedIn != status:
        
        if pluggedIn == 1:
            # switch to nvidia
            if get_curr_gpu() != 'nvidia':
                switch = boolbox('You are now plugged in. Would you like to switch to nvidia GPU?', 'Optimus Reminder', ['Do it automatically (Logout)', 'Do it manually'])
                
                if switch:
                    os.system('optimus-manager --switch nvidia --no-confirm')
            
            
        if pluggedIn == 0:
            #switch to intel
            if get_curr_gpu() != 'intel':

                switch = boolbox('You are no longer plugged in. Would you like to switch to intel GPU?', 'Optimus Reminder', ['Do it automatically (Logout)', 'Do it manually'])
                
                if switch:
                    os.system('optimus-manager --switch nvidia --no-confirm')

        file = open(os.path.join(DATA_DIR, FILENAME), 'w')
        file.write(str(pluggedIn))
        file.close()
        
    time.sleep(2)



    
