import asyncio
import threading
import datetime
import time
from queue import Queue
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import subprocess
from asyncua import Client, Node
import read_json
from google.api_core.exceptions import DeadlineExceeded
import read_json
import urllib.request
import socket

datachange_notification_queue_lock = asyncio.Lock()
class SubscriptionHandler:
    async def datachange_notification(self, node: Node, val, data):
        async with datachange_notification_queue_lock:
            if sub_flag:
                if node == READ_LAB["Power_on_AC"]:
                    if val == 1:
                        print("Power_on_AC")
                        mydict = {'col': 'R_cp_lab', 'doc': 'meeting_room',
                                  'field': 'AC', 'value': True}
                        firebase_queue.put(mydict)

                    else:   
                        print("Power_off_AC")
                        mydict = {'col': 'R_cp_lab', 'doc': 'meeting_room',
                                  'field': 'AC', 'value': False}
                        firebase_queue.put(mydict)
 

                elif node == READ_LAB["Power_on_AC1_W"]:
                    if val == 1:
                        print("Power_on_AC1_W")
                        mydict = {'col': 'R_cp_lab', 'doc': 'cpl',
                                  'field': 'AC1_W', 'value': True}
                        firebase_queue.put(mydict)

                    else:
                        print("Power_off_AC1_W")
                        mydict = {'col': 'R_cp_lab', 'doc': 'cpl',
                                  'field': 'AC1_W', 'value': False}
                        firebase_queue.put(mydict)

                elif node == READ_LAB["Power_on_AC_A"]: 
                    
                    if val == 1:
                        print("Power_on_AC_A")
                        mydict = {'col': 'R_cp_lab', 'doc': 'admin_room',
                                  'field': 'AC_A', 'value': True}
                        firebase_queue.put(mydict)

                    else:
                        print("Power_off_AC_A") 
                        mydict = {'col': 'R_cp_lab', 'doc': 'admin_room',
                                  'field': 'AC_A', 'value': False}
                        firebase_queue.put(mydict)

                # elif node == READ_LAB["AC_A"]: 
                    
                #     if val == 1:
                #         print("Power_on_AC_A")
                #         mydict = {'col': 'R_cp_lab', 'doc': 'admin_room',
                #                   'field': 'AC_A', 'value': True}
                #         plc_queue.put(mydict)

                #     else:
                #         print("Power_off_AC_A") 
                #         mydict = {'col': 'R_cp_lab', 'doc': 'admin_room',
                #                   'field': 'AC_A', 'value': False}
                #         plc_queue.put(mydict)
 

                elif node == READ_LAB["Power_on_Fan"]:
                    if val == 1:   
                        print("Power_on_Fan")
                        mydict = {'col': 'R_cp_lab', 'doc': 'meeting_room',
                                  'field': 'Fan', 'value': True}
                        firebase_queue.put(mydict)
 
                    else: 
                        print("Power_off_Fan")
                        mydict = {'col': 'R_cp_lab', 'doc': 'meeting_room',
                                  'field': 'Fan', 'value': False}
                        firebase_queue.put(mydict)
  

                elif node == READ_LAB["Power_on_Fan1_W"]:
                    if val == 1:  
                        print("Power_on_Fan1")
                        mydict = {'col': 'R_cp_lab', 'doc': 'cpl',
                                  'field': 'Fan1_W', 'value': True}
                        firebase_queue.put(mydict)
 
                    else: 
                        print("Power_off_Fan1")
                        mydict = {'col': 'R_cp_lab', 'doc': 'cpl',
                                  'field': 'Fan1_W', 'value': False}
                        firebase_queue.put(mydict)
 

                elif node == READ_LAB["Power_on_Fan2_W"]:  
                    if val == 1:
                        print("Power_on_Fan2")
                        mydict = {'col': 'R_cp_lab', 'doc': 'cpl',
                                  'field': 'Fan2_W', 'value': True}
                        firebase_queue.put(mydict)
 
                    else:
                        print("Power_off_Fan2")
                        mydict = {'col': 'R_cp_lab', 'doc': 'cpl',
                                  'field': 'Fan2_W', 'value': False}
                        firebase_queue.put(mydict)


                elif node == READ_LAB["Power_on_Fan3_W"]:
                    if val == 1:  
                        print("Power_on_Fan3")
                        mydict = {'col': 'R_cp_lab', 'doc': 'cpl',
                                  'field': 'Fan3_W', 'value': True}
                        firebase_queue.put(mydict)

                    else:
                        print("Power_off_Fan3")
                        mydict = {'col': 'R_cp_lab', 'doc': 'cpl',
                                  'field': 'Fan3_W', 'value': False}
                        firebase_queue.put(mydict)
 

                elif node == READ_LAB["Power_on_Fan4_W"]:  
                    if val == 1:
                        print("Power_on_Fan4")
                        mydict = {'col': 'R_cp_lab', 'doc': 'cpl',
                                  'field': 'Fan4_W', 'value': True}
                        firebase_queue.put(mydict)
 
                    else:  
                        print("Power_off_Fan4")
                        mydict = {'col': 'R_cp_lab', 'doc': 'cpl',
                                  'field': 'Fan4_W', 'value': False}
                        firebase_queue.put(mydict)


                elif node == READ_LAB["Power_on_Fan_A"]:
                    if val == 1:  
                        print("Power_on_Fan_A")
                        mydict = {'col': 'R_cp_lab', 'doc': 'admin_room',
                                  'field': 'Fan_A', 'value': True}
                        firebase_queue.put(mydict)
 
                    else:
                        print("Power_off_Fan_A")
                        mydict = {'col': 'R_cp_lab', 'doc': 'admin_room',
                                  'field': 'Fan_A', 'value': False}
                        firebase_queue.put(mydict)

                elif node == READ_LAB["Power_on_Lights_A"]:
                    
                    if val == 1:  
                        print("Power_on_Light_A") 
                        mydict = {'col': 'R_cp_lab', 'doc': 'admin_room',
                                  'field': 'Lights_A', 'value': True}
                        firebase_queue.put(mydict)

                    else: 
                        print("Power_off_Light_A")
                        mydict = {'col': 'R_cp_lab', 'doc': 'admin_room',
                                  'field': 'Lights_A', 'value': False}
                        firebase_queue.put(mydict)    

                # elif node == READ_LAB["Lights_A"]:
                    
                #     if val == 1:  
                #         print("Power_on_Light_A") 
                #         mydict = {'col': 'R_cp_lab', 'doc': 'admin_room',
                #                   'field': 'Lights_A', 'value': True}
                #         plc_queue.put(mydict)

                #     else: 
                #         print("Power_off_Light_A")
                #         mydict = {'col': 'R_cp_lab', 'doc': 'admin_room',
                #                   'field': 'Lights_A', 'value': False}
                #         plc_queue.put(mydict)
   

                elif node == READ_LAB["Power_on_Lights1_W"]:
                    if val == 1:      
                        print("Power_on_Lights1_W") 
                        mydict = {'col': 'R_cp_lab', 'doc': 'cpl',
                                  'field': 'Lights1_W', 'value': True}
                        firebase_queue.put(mydict)

                    else: 
                        print("Power_off_Lights1_W")
                        mydict = {'col': 'R_cp_lab', 'doc': 'cpl',
                                  'field': 'Lights1_W', 'value': False}
                        firebase_queue.put(mydict)


                elif node == READ_LAB["Power_on_Lights2_W"]:
                    if val == 1:  
                        print("Power_on_Lights2_W")
                        mydict = {'col': 'R_cp_lab', 'doc': 'cpl',
                                  'field': 'Lights2_W', 'value': True}
                        firebase_queue.put(mydict)
 
                    else:
                        print("Power_off_Lights2_W") 
                        mydict = {'col': 'R_cp_lab', 'doc': 'cpl',
                                  'field': 'Lights2_W', 'value': False}
                        firebase_queue.put(mydict)


                elif node == READ_LAB["Power_on_MPRC_W"]: 
                    if val == 1: 
                        print("Power_on_MPRC_W")
                        mydict = {'col': 'R_cp_lab', 'doc': 'machines',
                                  'field': 'MPRC_W', 'value': True}
                        firebase_queue.put(mydict)

                    else:
                        print("Power_off_MPRC_W")
                        mydict = {'col': 'R_cp_lab', 'doc': 'machines',
                                  'field': 'MPRC_W', 'value': False}
                        firebase_queue.put(mydict)


                elif node == READ_LAB["Power_on_AC2_W"]: 
                    if val == 1: 
                        print("Power_on_AC2_W")
                        mydict = {'col': 'R_cp_lab', 'doc': 'cpl',
                                  'field': 'AC2_W', 'value': True}
                        firebase_queue.put(mydict)

                    else:
                        print("Power_off_AC2_W") 
                        mydict = {'col': 'R_cp_lab', 'doc': 'cpl',
                                  'field': 'AC2_W', 'value': False}
                        firebase_queue.put(mydict)

                elif node == READ_LAB["Power_on_Station1_W"]: 
                    if val == 1: 
                        print("Power_on_Station1_W")
                        mydict = {'col': 'R_cp_lab', 'doc': 'machines',
                                  'field': 'Station1_W', 'value': True}
                        firebase_queue.put(mydict)
                    else:
                        print("Power_off_Station1_W")
                        mydict = {'col': 'R_cp_lab', 'doc': 'machines',
                                  'field': 'Station1_W', 'value': False}
                        firebase_queue.put(mydict) 

                elif node == READ_LAB["Power_on_Station2_W"]: 
                    if val == 1: 
                        print("Power_on_Station2_W")
                        mydict = {'col': 'R_cp_lab', 'doc': 'machines',
                                  'field': 'Station2_W', 'value': True}
                        firebase_queue.put(mydict) 
                    else:
                        print("Power_off_Station2_W")
                        mydict = {'col': 'R_cp_lab', 'doc': 'machines',
                                  'field': 'Station2_W', 'value': False}
                        firebase_queue.put(mydict) 

                elif node == READ_LAB["Power_on_Station3_W"]: 
                    if val == 1: 
                        print("Power_on_Station3_W")
                        mydict = {'col': 'R_cp_lab', 'doc': 'machines',
                                  'field': 'Station3_W', 'value': True}
                        firebase_queue.put(mydict)
                    else:
                        print("Power_off_Station3_W") 
                        mydict = {'col': 'R_cp_lab', 'doc': 'machines',
                                  'field': 'Station3_W', 'value': False}
                        firebase_queue.put(mydict) 

                elif node == READ_LAB["Power_on_T1_A"]: 
                    if val == 1: 
                        print("Power_on_T1_A")
                        mydict = {'col': 'R_cp_lab', 'doc': 'kits',
                                  'field': 'T1_A', 'value': True}
                        firebase_queue.put(mydict)
                    else:
                        print("Power_off_T1_A")
                        mydict = {'col': 'R_cp_lab', 'doc': 'kits',
                                  'field': 'T1_A', 'value': False}
                        firebase_queue.put(mydict)

                elif node == READ_LAB["Power_on_T2_A"]:
                    if val == 1:  
                        print("Power_on_T2_A")
                        mydict = {'col': 'R_cp_lab', 'doc': 'kits',
                                  'field': 'T2_A', 'value': True}
                        firebase_queue.put(mydict)
                    else:
                        print("Power_off_T2_A")
                        mydict = {'col': 'R_cp_lab', 'doc': 'kits',
                                  'field': 'T2_A', 'value': False}
                        firebase_queue.put(mydict)  

                elif node == READ_LAB["Power_on_kit1"]:
                    if val == 1:  
                        print("Power_on_kit1")
                        mydict = {'col': 'R_cp_lab', 'doc': 'kits',
                                  'field': 'Kit1', 'value': True}
                        firebase_queue.put(mydict)
                    else:
                        print("Power_off_kit1")
                        mydict = {'col': 'R_cp_lab', 'doc': 'kits',
                                  'field': 'Kit1', 'value': False}
                        firebase_queue.put(mydict) 
                          
                elif node == READ_LAB["Power_on_kit2"]: 
                    if val == 1: 
                        print("Power_on_kit2")
                        mydict = {'col': 'R_cp_lab', 'doc': 'kits',
                                  'field': 'Kit2', 'value': True}
                        firebase_queue.put(mydict)
                    else:
                        print("Power_off_kit2") 
                        mydict = {'col': 'R_cp_lab', 'doc': 'kits',
                                  'field': 'Kit2', 'value': False}
                        firebase_queue.put(mydict)  

                elif node == READ_LAB["Power_on_kit3"]:
                    if val == 1:  
                        print("Power_on_kit3")
                        mydict = {'col': 'R_cp_lab', 'doc': 'kits',
                                  'field': 'Kit3', 'value': True}
                        firebase_queue.put(mydict)
                    else:
                        print("Power_off_kit3")
                        mydict = {'col': 'R_cp_lab', 'doc': 'kits',
                                  'field': 'Kit3', 'value': False}
                        firebase_queue.put(mydict)

                elif node == READ_LAB["Power_on_kit4"]:
                    if val == 1:  
                        print("Power_on_kit4")
                        mydict = {'col': 'R_cp_lab', 'doc': 'kits',
                                  'field': 'Kit4', 'value': True}
                        firebase_queue.put(mydict)
                    else:
                        print("Power_off_kit4")
                        mydict = {'col': 'R_cp_lab', 'doc': 'kits',
                                  'field': 'Kit4', 'value': False}
                        firebase_queue.put(mydict)  

                elif node == READ_LAB["Power_on_kit5"]:
                    if val == 1:  
                        print("Power_on_kit5")
                        mydict = {'col': 'R_cp_lab', 'doc': 'kits',
                                  'field': 'Kit5', 'value': True}
                        firebase_queue.put(mydict)
                    else:
                        print("Power_off_kit5")
                        mydict = {'col': 'R_cp_lab', 'doc': 'kits',
                                  'field': 'Kit5', 'value': False}
                        firebase_queue.put(mydict)  

                elif node == READ_LAB["Power_on_kit6"]:
                    if val == 1:  
                        print("Power_on_kit6")
                        mydict = {'col': 'R_cp_lab', 'doc': 'kits',
                                  'field': 'Kit6', 'value': True}
                        firebase_queue.put(mydict)
                    else: 
                        print("Power_off_kit6")
                        mydict = {'col': 'R_cp_lab', 'doc': 'kits',
                                  'field': 'Kit6', 'value': False}
                        firebase_queue.put(mydict) 

                elif node == READ_LAB["Power_on_kit7"]:
                    if val == 1:  
                        print("Power_on_kit7")
                        mydict = {'col': 'R_cp_lab', 'doc': 'kits',
                                  'field': 'Kit7', 'value': True}
                        firebase_queue.put(mydict) 
                    else:
                        print("Power_off_kit7")
                        mydict = {'col': 'R_cp_lab', 'doc': 'kits',
                                  'field': 'Kit7', 'value': False}
                        firebase_queue.put(mydict) 

                elif node == READ_LAB["Power_on_kit8"]:
                    if val == 1:  
                        print("Power_on_kit8")
                        mydict = {'col': 'R_cp_lab', 'doc': 'kits',
                                  'field': 'Kit8', 'value': True}
                        firebase_queue.put(mydict)
                    else:
                        print("Power_off_kit8")
                        mydict = {'col': 'R_cp_lab', 'doc': 'kits',
                                  'field': 'Kit8', 'value': False}
                        firebase_queue.put(mydict)  

                elif node == READ_LAB["Power_on_lights"]:
                    if val == 1:  
                        print("Power_on_lights")
                        mydict = {'col': 'R_cp_lab', 'doc': 'meeting_room',
                                  'field': 'Light', 'value': True}
                        firebase_queue.put(mydict)
                    else:
                        print("Power_off_lights")
                        mydict = {'col': 'R_cp_lab', 'doc': 'meeting_room',
                                  'field': 'Light', 'value': False}
                        firebase_queue.put(mydict)  

                elif node == READ_LAB["Power_on_printer_W"]: 
                    if val == 1: 
                        print("Power_on_printer_W")
                        mydict = {'col': 'R_cp_lab', 'doc': 'machines',
                                  'field': 'printer_W', 'value': True}
                        firebase_queue.put(mydict)  
                    else:
                        print("Power_off_printer_W") 
                        mydict = {'col': 'R_cp_lab', 'doc': 'machines',
                                  'field': 'printer_W', 'value': False}
                        firebase_queue.put(mydict)   

                elif node == READ_LAB["Admin_Room_Temperature"]: 
                    if val < 25: 
                        print("Admin_Room_Temperature")
                        mydict = {'col': 'R_cp_lab', 'doc': 'admin_room',
                                  'field': 'normal_temp', 'value': True}
                        firebase_queue.put(mydict)  
                    else:
                        print("Admin_Room_Temperature") 
                        mydict = {'col': 'R_cp_lab', 'doc': 'admin_room',
                                  'field': 'normal_temp', 'value': False}
                        firebase_queue.put(mydict)
                
                elif node == READ_LAB["Compressor_O"]: 
                    if val == 1: 
                        print("Power_on_Compressor_I")
                        mydict = {'col': 'R_cp_lab', 'doc': 'other',
                                  'field': 'Compressor_I', 'value': True}
                        firebase_queue.put(mydict)  
                    else:
                        print("Power_on_Compressor_I") 
                        mydict = {'col': 'R_cp_lab', 'doc': 'other',
                                  'field': 'Compressor_I', 'value': False}
                        firebase_queue.put(mydict)

                elif node == READ_LAB["Open_Main_Door"]: 
                    if val == 1: 
                        print("Open_Main_Door")
                        mydict = {'col': 'R_cp_lab', 'doc': 'admin_room',
                                  'field': 'Main_Door', 'value': True}
                        firebase_queue.put(mydict)  
                    else:
                        print("Open_Main_Door") 
                        mydict = {'col': 'R_cp_lab', 'doc': 'admin_room',
                                  'field': 'Main_Door', 'value': False}
                        firebase_queue.put(mydict)        

def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host, timeout=8) # Set timeout to 1 second
        return True
    except urllib.error.URLError:
        return False
    except socket.timeout:
        return False
    
def init_firestore():
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate('firebase-admin-sdk.json')
            firebase_admin.initialize_app(cred)
        db_object = firestore.client()
        if db_object:
            print('Firestore connected')
            return db_object
        else:
            print('Error: Firestore not connected')
    except Exception as e:
        print(e)

def check_wifi_connection():
    print("Checking WiFi connection")
    output = subprocess.check_output(['iwconfig', 'wlo1']).decode('utf-8')
    return 'ESSID:"' in output

def check_iitd_wifi():
    print("Checking connectivity with IITD_WIFI")
    try:
        output = subprocess.check_output(['iwgetid'], text=True)
        ssid = output.strip().split(':')[1].strip('"')
        return ssid == 'IITD_WIFI'
    except subprocess.CalledProcessError:
        return False  # iwgetid command failed, not connected to any network

def connect_to_iitd_wifi():
    print("Connecting to IITD_WIFI")
    try:
        # Check if Wi-Fi is already disconnected
        if check_wifi_connection():
            subprocess.call(['nmcli', 'd', 'disconnect', 'wlo1'])

        # Turn off Wi-Fi
        subprocess.run(['nmcli', 'radio', 'wifi', 'off'])

        # Sleep for 1 minute
        time.sleep(60)

        # Turn on Wi-Fi
        subprocess.run(['nmcli', 'radio', 'wifi', 'on'])

        result = subprocess.run(['nmcli', 'device', 'wifi', 'connect', 'IITD_WIFI'], capture_output=True)
        # Check if the return code is 0, indicating success
        if result.returncode == 0:
            print("Connected to IITD_WIFI successfully.")
        else:
            print("Failed to connect to IITD_WIFI.")
    except Exception as e:
        print("Exception: " + str(e))
        # Check for Firestore Deadline Exceeded error
        if "firestoreDeadline of" in str(e):
            print("Firestore Deadline Exceeded error occurred. Waiting for 30 seconds before trying again...")
            time.sleep(30)

def check_network():
    connected = False

    while not connected:
        if check_iitd_wifi():
            if connect():
                print("Connected to IITD_WIFI")
                print("Checking WiFi IP")
                devices = subprocess.check_output(['nmcli', 'device', 'show', 'wlo1'])
                devices = devices.decode('ascii')
                devices = devices.split('\n')
                devices = [d for d in devices if 'IP4.ADDRESS' in d]
                if len(devices) > 0:
                    print("IP address found. Connected to IITD_WIFI")
                    connected = True
                else:
                    print("Connected to IITD WiFi but IP not found")
                    print("Disconnecting from IITD WiFi")
                    try:
                        subprocess.call(['nmcli', 'd', 'disconnect', 'wlo1'])
                    except Exception as e:
                        print("Error: " + str(e))

                    # Turn off Wi-Fi
                    print("Turning off Wi-Fi")
                    subprocess.run(['nmcli', 'radio', 'wifi', 'off'])

                    # Sleep for 1 minute
                    time.sleep(30)

                    # Turn on Wi-Fi
                    print("Turning on Wi-Fi")
                    subprocess.run(['nmcli', 'radio', 'wifi', 'on'])
            else:
                print("No internet!")  
                time.sleep(30)
                # connect_to_iitd_wifi()   
                       
        elif check_wifi_connection():
            print("Connected to other network, disconnecting...")
            try:
                subprocess.call(['nmcli', 'd', 'disconnect', 'wlo1'])
            except Exception as e:
                print("Error: " + str(e))
            connect_to_iitd_wifi()
        else:
            print("Not connected to any network, connecting to IITD_WIFI...")
            connect_to_iitd_wifi()

        if connected:
            return True
        else:
            # Sleep for 1 minute before attempting to connect again
            time.sleep(10)


async def push_updates_to_firestore(db):
    checkdict = {}
    try:
        while True:
            try:
                if not firebase_queue.empty():
                    my_dict = firebase_queue.get()
                    print(my_dict)
                    if checkdict != my_dict:
                        checkdict = my_dict
                        print(my_dict)
                        print("-----------")
                        print(my_dict['col'])
                        db.collection(my_dict['col']).document(my_dict['doc']).set(
                            {my_dict['field']: my_dict['value']}, merge=True)
                        print("*****data pushed to firestore*****")
                    elif my_dict == {'col': 'R_cp_lab', 'doc': 'admin_room', 'field': 'AC_A', 'value': True}:
                        print(my_dict['col'])
                        db.collection(my_dict['col']).document(my_dict['doc']).set(
                            {my_dict['field']: my_dict['value']}, merge=True)
                        print("*****data pushed to firestore*****")
                    elif my_dict == {'col': 'R_cp_lab', 'doc': 'admin_room', 'field': 'Lights_A', 'value': True}:
                        print(my_dict['col'])
                        db.collection(my_dict['col']).document(my_dict['doc']).set(
                            {my_dict['field']: my_dict['value']}, merge=True)
                        print("*****data pushed to firestore*****")
            except Exception as inner_e:
                print("An error occurred inside the while loop:", str(inner_e))
                # Handle the error here or re-raise it to propagate the exception
            
            await asyncio.sleep(0.1)
    except Exception as outer_e:
        print("Push updates to Firestore exception:", str(outer_e))
        
async def main():
    global READ_LAB
    case = 0
    subscription_handle_list = []
    run_once = 1
    while 1:
        if case == 1:
            try:
                if check_network():
                    print("Network available.")
                    case = 2
                else:
                    print("Network not available.")
                    case = 1
            except Exception as e:
                print("error in case 1: "+str(e))
                case = 1
                await asyncio.sleep(2)
        if case == 2:
            try:
                print("\nConnecting with LAB PLC")
                await  client_lab.connect()
                print("WS1 Connected!")
                case = 3
            except Exception as e:
                print("Connection error!" + str(e))
                case = 2
                await asyncio.sleep(2)
        elif case == 3:
            print("Case 3 Run")
            try:
                READ_LAB = read_json.get_nodes_read(client_lab)
                print('All nodes got filled ')
                case = 5
            except Exception as e:
                print("Exception: " + str(e))
                case = 3
                await asyncio.sleep(2)
        elif case == 5:
            # subscribe all nodes and events
            print("\nCreating Subscription ...")
            try:
                subscription = await client_lab.create_subscription(1000, SubscriptionHandler())
                for item in READ_LAB:
                    print('subscribing to ' + item)
                    handle = await subscription.subscribe_data_change(READ_LAB[item])
                    subscription_handle_list.append(handle)

                global sub_flag
                sub_flag = True
                print("\nAll Nodes of labautonomy Subscribed")
                case = 6
            except Exception as e:
                print("Main Exception " + str(e))
                case = 5
                await asyncio.sleep(2) 
        elif case == 6:
            try:
                service_level = await READ_LAB['State'].get_value()
                print("Service Level PLC: " + str(service_level))
                if service_level==0:
                    db.collection(u'R_code_tracking').document("python").update(
                        {"last_update": firestore.SERVER_TIMESTAMP})
                    print("Code status pushed to firebase at", datetime.datetime.now())
                    temp = await READ_LAB["Admin_Room_Temperature"].get_value()
                    print("Admin_Room_Temperature: ", temp)
                    mydict = {'col': 'R_cp_lab', 'doc': 'admin_room',
                                  'field': 'temperature_A', 'value': temp}
                    firebase_queue.put(mydict)
                    check_network()
                    case = 6
                    await asyncio.sleep(15)
                else:
                    print("in case 7 else")
                    case = 7
                await asyncio.sleep(2)
            except Exception as e:
                print("LAB PLC is Off!! Exception: " + str(e))
                case=7

        elif case == 7:
            # disconnect clean = unsubscribe, delete subscription then disconnect
            print("unsubscribing...")

            try:
                if subscription_handle_list:
                    for handle in subscription_handle_list:
                        await subscription.unsubscribe(handle)
                await subscription.delete()
                print("Unsubscribed!")
                case = 8
            except:
                print("unsubscribing error!")
                subscription = None
                subscription_handle_list = []
                await asyncio.sleep(0)
                case = 8
        elif case == 8:
            print("Disconnecting...")
            try:
                await client_lab.disconnect()
                
            # case = 1
            except Exception as e:
                print("Disconnection exception: " + str(e))
            case = 0
        else:
            # wait
            case = 1
            await asyncio.sleep(1)
          


if __name__ == '__main__':
    sub_flag = False
    plc_queue = Queue(maxsize=0)
    firebase_queue = Queue(maxsize=0)
    READ_LAB={}
    client_lab = Client("opc.tcp://10.226.52.207:4840")
    db = init_firestore()
    
    # create the event loop
    loop = asyncio.get_event_loop()
    task_main = loop.create_task(main())

    task_firestore = loop.create_task(push_updates_to_firestore(db))
    asyncio.gather(task_main,task_firestore)

    
    try:
        loop.run_forever()
    finally:
        loop.close()

        