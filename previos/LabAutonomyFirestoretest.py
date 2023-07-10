#pip3 install firebase-admin
#pip3 install asyncua
#pip3 install pandas

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
from asyncua import Client
import read_json
from google.api_core.exceptions import DeadlineExceeded


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
    print("Checking WiFi_connection")
    output = subprocess.check_output(['iwconfig', 'wlo1']).decode('utf-8')
    if 'ESSID:"' in output:
        return True
    else:
        return False
    
def check_iitd_wifi():
    print("Checking connectivity with iitd_WiFi")
    result = subprocess.run(['iwgetid'], capture_output=True, text=True)
    if result.returncode != 0:
        return False  # iwgetid command failed, not connected to any network
    ssid = result.stdout.strip().split(':')[1].strip('"')
    return ssid == 'IITD_WIFI'

def check_network():
    case = 0
    while True:
        if case == 1:
            if check_iitd_wifi():
                # print(subprocess.call(['nmcli', 'd', 'disconnect', 'wlo1']))
                print("Checking WiFi IP")
                devices = subprocess.check_output(['nmcli', 'device', 'show', 'wlo1'])
                devices = devices.decode('ascii')
                devices = devices.split('\n')
                devices = [d for d in devices if 'IP4.ADDRESS' in d]
                if len(devices) > 0:
                    print("Connected to IITD_WIFI")
                    return True
                else:
                    print("Connected to IITD WiFi but IP does not found")
                    print("Connecting to MTNLFSM-5GHZ WiFi")
                    subprocess.call(['nmcli', 'd', 'disconnect', 'wlo1'])
                    subprocess.call(['nmcli', 'd', 'connect', 'MTNLFSM-5GHZ'])
                    result = subprocess.run(['nmcli', 'device', 'wifi', 'connect', 'MTNLFSM-5GHZ'], capture_output=True)

                    # Check if the return code is 0, indicating success
                    if result.returncode == 0:
                        print("Connected to MTNLFSM-5GHZ successfully.")
                    else:
                        print("Failed to connect to MTNLFSM-5GHZ.")
                    time.sleep(0.5)
                    case = 2
            else:
                print('Not connected to IITD_WIFI')     
                case = 2
        elif case == 2:
            if check_wifi_connection(): 
                try:
                    print("Not Connected to IITD WiFi")
                    print("Disconnecting")
                    subprocess.call(['nmcli', 'd', 'disconnect', 'wlo1'])
                except Exception as e:
                    print("Exception: " + str(e))
            else:
                print('Not Connected to any network')
            
            print("Connecting to IITD_WIFI")
            try:
                result = subprocess.run(['nmcli', 'device', 'wifi', 'connect', 'IITD_WIFI'], capture_output=True)
                # Check if the return code is 0, indicating success
                if result.returncode == 0:
                    print("Connected to IITD_WIFI successfully.")
                else:
                    print("Failed to connect to IITD_WIFI.")         
                case=1
            except Exception as e:
                print("Exception: " + str(e))
                case = 1

        elif case == 0:
            time.sleep(0.5)
            case = 1


# called in main loop
async def get_latest_values_from_plc():
    time.sleep(1)
    print("Getting latest data from the PLC")
    # getting current value from PLC
    for key in nodes_dict_lab:
        if key in admin_room_dict.keys():
            lab_dict['admin_room'][key] = await nodes_dict_lab[key].get_value()
        elif key in cpl_dict.keys():
            lab_dict['cpl'][key] = await nodes_dict_lab[key].get_value()
        elif key in kits_dict.keys():
            lab_dict['kits'][key] = await nodes_dict_lab[key].get_value()
        elif key in machines_dict.keys():
            lab_dict['machines'][key] = await nodes_dict_lab[key].get_value()
        elif key in meeting_room_dict.keys():
            lab_dict['meeting_room'][key] = await nodes_dict_lab[key].get_value()
        elif key in other_dict.keys():
            lab_dict['other'][key] = await nodes_dict_lab[key].get_value()
        elif key in sensors_dict.keys():
            lab_dict['sensors'][key] = await nodes_dict_lab[key].get_value()


# called in main loop
def push_updates_to_firestore():
    print("push_updates_to_firestore at", datetime.datetime.now())
    try:
        check_network()
        print('in push updates')
        db_o = init_firestore()
        print("Firebase Object Created")
        firebase_ref_dict = {}
        for key in lab_dict:
            firebase_ref_dict[key] = db_o.collection(u'cp_lab').document(key)
        print("Uploading to Firestore")
        for room in lab_dict:
            for switch in lab_dict[room]:
                firebase_ref_dict[room].update({switch: lab_dict[room][switch]})
        print("Firestore Updated")
    except DeadlineExceeded as ex:
        print("Deadline exceeded error: ", str(ex))
        check_network()
        time.sleep(1) 
        # push_updates_to_firestore()  # retry    
    except Exception as ex:
        print("exception in push update firestore"+str(ex))
        check_network()

# Callback on_snapshot function to capture changes from firebase
def on_snapshot(col_snapshot, changes, read_time):
    print(u'Callback received query snapshot.')
    for change in changes:
        if change.type.name == 'MODIFIED':
            doc_dir = change.document.to_dict()
            print(doc_dir)
            plc_queue.put(doc_dir)
            
    callback_done.set()


# need to call in starting
async def plc_execute():
    await asyncio.sleep(10)
    print("in plc execute")
    while True:
        await asyncio.sleep(0.01)
        # print("in while true loop")
        if not plc_queue.empty():
            doc_dir = plc_queue.get()
            # print(doc_dir)
            for key in doc_dir:
                await nodes_dict_lab[key].set_value(doc_dir[key])


async def main():
    await asyncio.sleep(0.01)
    print("In main")
    db_o = init_firestore()
    case = 0
    subscription_handle_list = []
    idx = 0
    while 1:
        if case == 1:
            check_network()
            try:
                print("\nConnecting with LAB PLC")
                await client_lab.connect()
                print("LAB PLC Connected!")
                case = 2
            except Exception as e:
                print("Connection error! Exception:" + str(e))
                case = 1
                await asyncio.sleep(2)
        elif case == 2:
            print("Case 2 Run")
            try:
                global nodes_dict_lab
                nodes_dict_lab = read_json.get_lab_nodes(client_lab)
                case = 5
            except Exception as e:
                print("Exception: " + str(e))
                case = 2
                await asyncio.sleep(2)
        elif case == 5:
            print("Case 5")
            try:
                await get_latest_values_from_plc()
                case = 6
            except Exception as e5:
                print("Case 5: " + str(e5))
                case = 4
        elif case == 6:
            print("Case 6")
            try:
                service_level = await nodes_dict_lab['State'].get_value()
                if service_level==0:
                    push_updates_to_firestore()
                    case = 3
                else:
                    print("PLC Check node off")
                    case = 4
            except Exception as e6:
                print("Case 5: " + str(e6))
                case = 4
        elif case == 3:
            print("in case 3")
            try:
                service_level = await nodes_dict_lab['State'].get_value()
                print("Service Level PLC: " + str(service_level))
                if service_level==0:
                    db_o.collection(u'code_tracking').document("python").update(
                        {"last_update": firestore.SERVER_TIMESTAMP})
                    print("Code status pushed to firebase at", datetime.datetime.now())
                    check_network()
                    case = 3
                    await asyncio.sleep(15)
                else:
                    print("in case 3 else")
                    case = 4
                await asyncio.sleep(2)
            except Exception as e:
                print("LAB PLC is Off!! Exception: " + str(e))
                case=4
        elif case == 4:
            print("in case 4")
            print("Disconnecting...")
            try:
                await client_lab.disconnect()
            except Exception as e:
                print("Disconnection Error! Exception: " + str(e))
            case = 0
        else:
            # wait
            case = 1
            await asyncio.sleep(2)


if __name__ == '__main__':

    admin_room_dict = {'AC_A': True, 'Fan_A': True, 'Lights_A': True, 'Main_Door': True}
    cpl_dict = {'AC1_W': True, 'AC2_W': True, 'Fan1_W': True, 'Fan2_W': True, 'Fan3_W': True, 'Fan4_W': True,
                'Lights1_W': True, 'Lights2_W': True}
    kits_dict = {'Kit1': True, 'Kit2': True, 'Kit3': True, 'Kit4': True, 'Kit5': True, 'Kit6': True, 'Kit7': True,
                 'Kit8': True, 'T1_A': True, 'T2_A': True}
    machines_dict = {'MPRC_W': True, 'Station1_W': True, 'Station2_W': True, 'Station3_W': True, 'printer_W': True}
    meeting_room_dict = {'AC': True, 'Fan': True, 'Light': True}
    other_dict = {'Compressor_I': False}
    sensors_dict = {'IITD_Mains': True}

    lab_dict = {
        'admin_room': admin_room_dict,
        'cpl': cpl_dict,
        'kits': kits_dict,
        'machines': machines_dict,
        'meeting_room': meeting_room_dict,
        'other': other_dict,
        'sensors': sensors_dict,
    }

    client_lab = ''
    nodes_dict_lab = {}
    update_firestore_flag = False
    plc_queue = Queue(maxsize=0)
    # t = threading.Thread(target=check_network)
    # t.start()

    if check_network():
        client_lab = Client("opc.tcp://10.226.52.207:4840")
    else:
        print('Network Issue')

    # Create an Event for notifying main thread.
    db = init_firestore()
    callback_done = threading.Event()
    col_query = db.collection(u'cp_lab')
    doc_watch = col_query.on_snapshot(on_snapshot)
    
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(main())
    asyncio.ensure_future(plc_execute())
    loop.run_forever()
