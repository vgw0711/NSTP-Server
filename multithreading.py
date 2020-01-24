
# import socket programming library 
import socket 
import hashlib
# import thread module 
from _thread import *
import threading 

key_value_store = {}                #Test case : Run two clients while printing dictionary on both of them

#T,L(M),M

def error_message():
   error_response = b'\x02\x00\x05error'
   return error_response

def hasher(hash_value , hash_algo):
   if hash_algo == b'\x00' :
     return hash_value
   elif hash_algo == b'\x01' :
     return hashlib.sha256(hash_value).digest()
   elif hash_algo == b'\x02' :
     return hashlib.sha512(hash_value).digest()
   return -1   

def store_data(key,value):
   try:
      key_value_store[key] = value
      print("Stored {} in key {}".format(value,key))
      return 1
   except:
      return -1

def load_handler(payload):
   try:
      l = hex(payload[1])+format(payload[2],'x')     #Combine the lengths
      length_key = int(l,0)                              #length of key
      key = payload[3:length_key+3]
      if(length_key+3 == len(payload)):
         try:
            val = key_value_store.get(key)
            resource_length = bytes.fromhex("{:04x}".format(len(val)))
            load_response = b'\x06' + resource_length + val
            return load_response
         except:
            val = b''
            return b'\x06\x00\x00'+val      
   except:
      print("Request verification failed")   
   return -1


def store_handler(payload):
   try:
      l = hex(payload[1])+format(payload[2],'x')     #Combine the lengths
      length_key = int(l,0)                              #length of key
      v = hex(payload[length_key+3])+format(payload[length_key+4],'x')     #Combine the lengths
      length_value = int(v,0)                    #length of key
      if(length_key+length_value+5 == len(payload)):
         store_status = store_data(payload[3:length_key+3],payload[length_key+5:length_key+length_value+5])
         if(store_status == 1):
            value_hash = hasher(payload[length_key+5:length_key+length_value+5],b'\x01')
            hash_length = b'\x00\x20'
            hash_algo = b'\x01'
            store_response = b'\x08'+hash_length+value_hash+hash_algo
            return store_response
   except:
      print("Request verification failed")   
   return -1

def client_hello_handler(payload):
   try:
      major_version = payload[1]
      l = hex(payload[3])+format(payload[4],'x')     #Combine the lengths
      length = int(l,0) #Length of user agent in integer
      minor_version = payload[2:3]
      user_agent = payload[5:len(payload)]
      if(major_version == 1 and length + 5 == len(payload)):
         server_hello = b'\x01\x01'+minor_version+payload[3:4]+payload[4:5]+user_agent
         return server_hello 
   except:
      print("Request verification failed")   
   return -1

def ping_handler(payload):
   try:
      l = hex(payload[1])+format(payload[2],'x')     #Combine the lengths
      length = int(l,0) #Length of to_be_hashed  in integer
      #print("Hex length {}, Int Length {}".format(repr(l),str(length)))
      to_be_hashed = payload[3:length+3] 
      hash_algo = payload[length+3:]
      if(length+3 == len(payload)-1):
         if(hash_algo == b'\x00'):
            ping_hash = hasher(to_be_hashed , hash_algo)
            ping_response = b'\x04'+payload[1]+payload[2]+ping_hash
            return ping_response
         elif(hash_algo == b'\x01'):
            ping_hash = hasher(to_be_hashed , hash_algo)
            ping_response = b'\x04\x00\x20'+ping_hash
            return ping_response 
         elif(hash_algo == b'\x02'):
            ping_hash = hasher(to_be_hashed , hash_algo)
            ping_response = b'\x04\x00\x40'+ping_hash 
            return ping_response
   except:
      print("Request verification failed")   
   return -1


def recv_input(c , c_e):
   input_val = c.recv(5096)
   ret_val , c_e = process_input(input_val , c_e)
   return ret_val , c_e

def process_input(input_val , c_e):
   response = b''
   if(input_val[0] == 0):
      c_e = 1
      return client_hello_handler(input_val) , c_e
   elif(c_e == 1):
      if(input_val[0]  == 3):
         return ping_handler(input_val) , c_e
      elif(input_val[0] == 5):
         return load_handler(input_val) , c_e
      elif(input_val[0] == 7):
         return store_handler(input_val) , c_e
   response = -1
   print("Breaking you because your request doesn't follow the protocol ... response : {}".format(response))
   return response , c_e

# thread function 
def threaded(c): 
   try:
      conn_est = 0    #Conn_established = 0(false) 1(true) 
      c.settimeout(10.0)  #Taking care of DOS attacks
      while True: 
         try: 
            data , conn_est = recv_input(c , conn_est)
            if(data == -1):
              break
         except:
            print("Problem with the pipe.")
            break   
         print(data)
         c.send(data)
   except:
      c.close()  
   c.close() 

def Main(): 
   host = "0.0.0.0" 
   port = 22307
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
   s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   try:
      s.bind((host, port))
      print("socket binded to port", port) 
   except:
      print("Socket Bind Error") 
   s.listen() 
   print("socket is listening") 
   # a forever loop until client wants to exit 
   while True: 
      # establish connection with client 
      c, addr = s.accept() 
      print('Connected to :', addr[0], ':', addr[1]) 
      # Start a new thread and return its identifier 
      try:
         start_new_thread(threaded, (c,))
      except:
         print("Some problem with starting the thread.") 
   s.close() 


if __name__ == '__main__': 
   Main() 
