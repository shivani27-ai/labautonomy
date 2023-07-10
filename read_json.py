import pandas as pd
from asyncua import Client


def read_file():
    try:
        dataset = pd.read_csv('Lab_Auto_Nodes_CSV.csv')
        variable_names = dataset.iloc[:, 1].values
        node_address = dataset.iloc[:, 3].values
        return variable_names, node_address
    except FileNotFoundError:
        print("\nFile not found")
    except PermissionError:
        print("\nYou don't have the permission to read the file")
    except Exception as ex:
        TEMP = "An exception of type {0} occurred. Arguments:\n{1!r}"
        MESSAGE = TEMP.format(type(ex).__name__, ex.args)
        print(MESSAGE)


def get_lab_nodes(client_lab):
    try:
        variable_names, node_address = read_file()
        NODES_DICT_LAB = {}
        NODES_DICT_LAB["State"] = client_lab.get_node("i=2259")
        for (name, address) in zip(variable_names, node_address):
            address = address.replace('Node(StringNodeId(', '').replace('))', '')
            if 'Power_on_' not in name:
                NODES_DICT_LAB[name] = client_lab.get_node(address)
        return NODES_DICT_LAB
    except Exception as e:
        print(e)


def read_file2():
    try:
        dataset = pd.read_csv('readnodes.csv')
        VARIABLE_NAMES = dataset.iloc[:, 0].values
        NODE_ADDRESS = dataset.iloc[:, 1].values
        return VARIABLE_NAMES,NODE_ADDRESS 
    except FileNotFoundError:
        print("\nFile not found")
    except PermissionError:
        print("\nYou don't have the permission to read the file")
    except Exception as ex:
        TEMP = "An exception of type {0} occurred. Arguments:\n{1!r}"
        MESSAGE = TEMP.format(type(ex).__name__, ex.args)
        print(MESSAGE)

def get_nodes_read(client_lab): 
    LAB_DICT = {} 
    try:
        variable_names, node_address = read_file2()
        LAB_DICT["State"] = client_lab.get_node("i=2259")
        for (node_name, address) in zip(variable_names,node_address):
            address = address.replace('Node(StringNodeId(', '').replace('))', '')
            LAB_DICT[node_name] = client_lab.get_node(address)
            
        return LAB_DICT       
    except Exception as e:
        print(e)
       

