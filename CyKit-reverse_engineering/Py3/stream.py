# CyKit 1.0 for Python 3.3 
# (Raw TCP Stream) 14 Signed Integers delimited(spaced) by period + CRLF
# 
#  Supported Model: EPOC
#
#  Project is deprecated. Please use THE latest version for (Python 3)

import socket
import gevent
import sys
#sys.path.insert(1, './Python/CyKit/')
import emotiv
if len(sys.argv) < 3 or len(sys.argv) < 2:
   print("Usage:  Python.exe stream.py IP Port")
   sys.argv = [sys.argv[0], "localhost", "5555"]
   print("Defaulting to localhost:5555")
   
def main():

    try:         
         

         connectServer()
                  
    except exc as e:
         print(e)

    gevent.sleep(1)
    try:
       while True: 
             packet = headset.dequeue()

             connbuffer = ""
             gevent.sleep(.001)
             for name in 'AF3 F7 F3 FC5 T7 P7 O1 O2 P8 T8 FC6 F4 F8 AF4'.split(' '):
              
              v = packet.sensors[name]['value']
              connbuffer += str(v) + "."
             connbuffer += "\r\n"
             conn.sendall(connbuffer.encode('utf-8'))
             connbuffer = ""
             
    except Exception as msg:
             print("Streaming Error: ", sys.exc_info()[0],  sys.exc_info()[1],  sys.exc_info()[2], " : ",  msg)
             conn.close()
             #headset.kill()
    finally:
             print("Disconnecting . . .")
             conn.close()
             gevent.GreenletExit
             print("Restarting . . .")
             main()


def connectServer():
     global conn
     HOST = str(sys.argv[1])
     PORT = int(sys.argv[2])
     print("Listening to ", HOST, " : ", str(PORT))
     try:
         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     except socket.error as msg:
         s = None

     try:
         s.bind((HOST, PORT))
         s.listen(1)
     except socket.error as msg:
         s.close()
         s = None

     if s is None:
         print('Could not open socket')
         return
     
     conn, addr = s.accept()
     print('Listening to', addr)
     

try:
  headset = emotiv.Emotiv(True, False)
  gevent.spawn(headset.setup_windows)
  main()

except Exception as e:
  exc = e
  print(" @ @ @ ", e)
  print("Device Time Out or Disconnect . . .    Reconnect to Server.")
  conn.close()
  main()
