# Import socket module 
import socket 
import time

def Main(): 
   # local host IP '127.0.0.1' 
   host = '127.0.0.1'

   # Define the port on which you want to connect 
   port = 22304

   s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 

   # connect to server on local computer 
   s.connect((host,port)) 

   # message you send to server 
   message=b'\x00\x01\x01\x00\x0bvisha visha'
   while True: 
      # message sent to server 
      try:
         for i in range(300):
            s.send(message)   #message.encode('ascii') 
            data = s.recv(1024)
            if data:
               print('Received from the server :',repr(data))  #str(data.decode('ascii'))
            for i in range(1):
               print(str(i))
               time.sleep(1)
            message = b'\x07\x00\x02vi\x00\x04vish'
      except:
         print("Some error occured")
         break
         # messaga received from server 
       

      # print the received message 
      # here it would be a reverse of sent message 
       

      # ask the client whether he wants to continue 
      #ans = input('\nDo you want to continue(y/n) :') 
      #if ans == 'y': 
      #  continue
      #else: 
      #  break
   # close the connection 
   s.close() 

if __name__ == '__main__': 
   Main() 
