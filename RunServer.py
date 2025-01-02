########### SLEEPY CODE


# LISTEN IS SUPPOSE TO ALLOW TO LISTEN TO IID
# I START WITH PUSH THEN I WILL DO LISTEN


# WARNING: IN THIS CODE I CONSIDER THAT YOU HAVE A SMALL COMMUNITY OF USERS
# THIS IS NOT DESIGN FOR A BIG COMMUNITY, ELSE YOU WILL NEED RUST CODE AND  FOLK


#import iidwshandshake # https://github.com/EloiStree/2025_01_01_MegaMaskSignInHandshake_Python/tree/main

# pip install web3
import socket
import threading
from web3 import Web3
import os
from eth_account.messages import encode_defunct
import uuid

import os
import sys
import uuid
import asyncio
import websockets
import struct
import requests

w3 = Web3()



in_udp_port = 4625



RTFM= "https://github.com/EloiStree/2025_01_01_MegaMaskSignInHandshake_Python.git"

print("Hello World Python IID Listen Server")
user_index_public_index_file = "/git/APIntIO_Claim/Claims"


# read the file
user_index_to_address={}
user_address_to_index={}

with open(user_index_public_index_file, 'r') as file:
    text = file.read()
    lines = text.split("\n")
    for line in lines[:20]:
        if ":" in line:
            index, address = line.split(":")
            user_index_to_address[index] = address
            user_address_to_index[address] = index
            
print (f"Claimed index: {len(user_index_to_address)}")
dict_size = sys.getsizeof(user_index_to_address)
for key, value in user_index_to_address.items():
    dict_size += sys.getsizeof(key) + sys.getsizeof(value)
dico_size_in_mo = int(int(dict_size) / 1024 / 1024*10000) / 10000
print(f"Byte size of user_index_to_address: {dict_size}, {dico_size_in_mo} Mo")




bool_use_byte_count = True
byte_count_ip="127.0.0.1"
byte_count_port=666
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
byte_count_target=  (byte_count_ip, byte_count_port)

def byte_count(index_integer:int, byte_count:int):
    sock.sendto(struct.pack('<ii', index_integer, byte_count),byte_count_target )
    


def is_message_signed(given_message):
    
    split_message = given_message.split("|")
    if len(split_message) < 3:
        return False
    message = split_message[0]
    address = split_message[1]
    signature = split_message[2]
    return is_message_signed_from_params(message, address, signature )

def is_message_signed_from_params(message, address, signature):
    # Message to verify

    # Encode the message
    encoded_message = encode_defunct(text=message)

    # Recover the address from the signature
    recovered_address = w3.eth.account.recover_message(encoded_message, signature=signature)
    return  recovered_address.lower() == address.lower()

def get_address_from_signed_message(given_message):
    split_message = given_message.split("|")
    if len(split_message) < 3:
        return None
    return split_message[1]


class UserHandshake:
    def __init__(self):
        self.index = index
        self.address = address
        self.handshake_guid = uuid.uuid4()
        self.remote_address = None          
        self.waiting_for_clipboard_sign_message = False
        self.is_verified = False       
        self.websocket= None       
        
        
        
                
guid_handshake = {}
index_to_user={}

bool_use_debug_print = True
def debug_print(text):
    if bool_use_debug_print:
        print(text)
        
        
bool_only_byte_server = False
int_max_byte_size = 16
async def hangle_text_message(user:UserHandshake, message:str):
    if not bool_only_byte_server:
        user.websocket.send(f"ONLY BYTE SERVER AND MAX:{int_max_byte_size}")
        user.websocket.send(f"RTFM:{RTFM}") 
        user.websocket.close()
        return
    print("Received text message", message)
    
    
async def handle_byte_message(user:UserHandshake, message:bytes):
    if len(message) > int_max_byte_size:
        user.websocket.send(f"MAX BYE SIZE {int_max_byte_size}")
        user.websocket.send(f"RTFM:{RTFM}") 
        user.websocket.close()
        return
    print("Received byte message", len(message))

async def handle_connection(websocket, path):
    debug_print(f"New connection from path {path}")
    debug_print(f"New connection from address {websocket.remote_address}")
    user : UserHandshake = UserHandshake()
    user.remote_address = websocket.remote_address    
    user.websocket= websocket
    await websocket.send(f"MANUAL:{RTFM}")
    await websocket.send(f"SIGN:{user.handshake_guid}")
    user.waiting_for_clipboard_sign_message = True
    while True:    
        try:
            async for message in websocket:
                if user.waiting_for_clipboard_sign_message:
                    if not is_message_signed(message):
                        await websocket.send(f"FAIL TO SIGN")
                        await websocket.close()
                    address = get_address_from_signed_message(message)
                    print (f"User {user.address} signed the handshake")
                   
                    user.address = address
                    if address not in user_address_to_index:
                        await websocket.send(f"ASK ADMIN FOR A CLAIM TO BE ADDED")
                        await websocket.send(f"RTFM:{RTFM}")
                        await websocket.close()
                    user.index = user_address_to_index[address]
                    user.is_verified = True
                    user.waiting_for_clipboard_sign_message = False
                    guid_handshake[user.handshake_guid] = user
                    index_to_user[str(user.index)] = user
                    await websocket.send(f"HELLO {user.index} {user.address}")
                else:
                    if isinstance(message, str):
                        await hangle_text_message(user, message)
                    else:
                        await handle_byte_message(user, message)
                    if bool_use_byte_count:
                        byte_count(int(user.index), len(message))
                    
                    
        except websockets.ConnectionClosed:
            print(f"Connection closed from {websocket.remote_address}")



def loop_start_websocket_server():
    asyncio.run(main())


async def main():
    server = await websockets.serve(handle_connection, "0.0.0.0", 4616)
    print("WebSocket server started on ws://0.0.0.0:4616")
    await server.wait_closed()



in_udp_ip= "127.0.0.1"

def loop_start_udp_server():
    asyncio.run(start_udp_server())
  
async def start_udp_server():
    global index_to_user
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((in_udp_ip, in_udp_port))
    print(f"UDP server started on {in_udp_ip}:{in_udp_port}")
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Received {data} from {addr}")
        l = len(data)
        if l == 16:
            index, value, date = struct.unpack('<iiQ', data)
            index_str = str(index)
            print(f"Received {index} {value} {date} from {addr}")
            if index_str in index_to_user:
                user = index_to_user[index_str]
                await user.websocket.send(data)
                print(f"data: {data}")
            else:
                print(f"User {index} not found")
        
    


def get_public_ip():
        response = requests.get('https://api.ipify.org?format=json')
        return response.json()['ip']

    
        
if __name__ == "__main__":
    
    public_ip = get_public_ip()
    print(f"Public IP: {public_ip}")
    # Create threads
    thread1 = threading.Thread(target=loop_start_udp_server)
    thread2 = threading.Thread(target=loop_start_websocket_server)
    
    # Start threads
    thread1.start()
    thread2.start()
    
    # Wait for threads to complete (optional; keeps main program alive)
    thread1.join()
    thread2.join()