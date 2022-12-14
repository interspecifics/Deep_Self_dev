# -*- coding: utf8 -*-
#
#  CyKIT  2021.03.12
#  ________________________
#  example_insight_v2.py
#
#  For all Insight models.
#  Software Firmware: 0x925 and 0x932 
# 
#  Written by Warren
#
"""

  usage:  python.exe .\example_insight_v2.py
   
"""   
   
import sys, os, time, threading

sys.path.insert(0, '..//py3//cyUSB//cyPyWinUSB')
sys.path.insert(0, '..//py3')

import cyPyWinUSB as hid
import queue
from cyCrypto.Cipher import AES
from cyCrypto import Random

import io
import argparse
from datetime import datetime as dt

tasks = queue.Queue()
EEG_name = { "AF3":3, "T7": 5, "Pz":7, "T8":12, "AF4":14 }

# optional CLI parameter to add a username to the resulting csv filename
parser = argparse.ArgumentParser(description="Program to record EEG data to csv",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-u", "--user", default='', help="namer of user being monitored")
args = vars(parser.parse_args())

# creating csv
user = args['user']
filename = "recordings/" + user + "EEG " + str(dt.now())[:-7] + ".csv"
filename = filename.replace(' ', '_').replace(':','')
with open(filename, 'w') as f:
    f.write("counter,AF3,T7,Pz,T8,AF4\n")


class EEG_insight(object):
   
    def __init__(self):
        self.hid = None
        devicesUsed = 0

        self.cipher = None
        for device in hid.find_all_hid_devices():
                if device.product_name == 'EEG Signals':
                    devicesUsed += 1
                    self.hid = device
                    self.hid.open()
                    self.serial_number = device.serial_number
                    device.set_raw_data_handler(self.dataHandler)                   
        if devicesUsed == 0:
            os._exit(0)
        
        sn = bytearray()
        for i in range(0,len(self.serial_number)):
            sn += bytearray([ord(self.serial_number[i])])

        # Insight Keymodel.
        k = ['\0'] * 16
        k = [sn[-1],00,sn[-2],21,sn[-3],00,sn[-4],12,sn[-3],00,sn[-2],68,sn[-1],00,sn[-2],88]

        self.key = bytes(bytearray(k))
        self.cipher = AES.new(self.key, AES.MODE_ECB)
        

    def dataHandler(self, data):
        if self.cipher == None:
            return
        join_data = ''.join(map(chr, data[1:]))
        data = self.cipher.decrypt(bytes(join_data,'latin-1')[0:32])
        tasks.put(data)
      
    def convert_v2(self, value_1, value_2):
        edk_value = "%.8f" % (((int(value_1) -128) * 32.82051289) + ((int(value_2) * .128205128205129) + 4201.02564096001))
        return edk_value
       
    def get_data(self):
        
        try:
            data = tasks.get()
            data = tasks.get() # Pops (and disposes, of an EEG packet) to keep data updating in real-time.
                               # Remove extra tasks.get() for accuracy.
                               
            packet_data = [data[0]]
            z = ''
            for i in range(1,len(data)):
                z = z + format(data[i],'08b')
            
            i_1 = -14
            for i in range(0,18):
                i_1 += 14
                v_1 = '0b' + z[(i_1):(i_1 + 8)]
                v_2 = '0b' + z[(i_1 + 8):(i_1 + 14)]
                packet_data.append(str(self.convert_v2(str(eval(v_1)),str(eval(v_2)))))
            return packet_data
          
        except Exception as exception2:
            print(str(exception2))

    def update_screen(self):
        counter = 0
        while 1:
            eeg_data = cyHeadset.get_data()
            
            """
            Debugging. To see all the unformatted EEG/Gyro data. 
            print(str(eeg_data)) 
            """
            
            print("  AF3 = " + str(eeg_data[EEG_name["AF3"]]) + "mV\r\n")
            print("   T7 = " + str(eeg_data[EEG_name["T7"]])  + "mV\r\n")
            print("   Pz = " + str(eeg_data[EEG_name["Pz"]])  + "mV\r\n")
            print("   T8 = " + str(eeg_data[EEG_name["T8"]])  + "mV\r\n")
            print("  AF4 = " + str(eeg_data[EEG_name["AF4"]]) + "mV\r\n")
            
            # write to csv
            # column order is "counter,AF3,T7,Pz,T8,AF4"
            line = [
                str(counter % 128),
                eeg_data[EEG_name["AF3"]],
                eeg_data[EEG_name["T7"]],
                eeg_data[EEG_name["Pz"]],
                eeg_data[EEG_name["T8"]],
                eeg_data[EEG_name["AF4"]]
            ]

            # import pdb; pdb.set_trace()
            with open(filename, 'a') as f:
                f.write(','.join(line) + "\n")

            counter += 1

            time.sleep(.001)
            print("\r\n")

if os.name == 'nt':
    os.system("mode con:cols=80 lines=14")  # Resize screen (for Windows)

cyHeadset = EEG_insight()
eeg_data = []
data_thread = threading.Thread(name = " Update_EEG_Headset", target = cyHeadset.update_screen, daemon = False ) 
init = True


while 1:
    
    if init == True:
        data_thread.start()
        init = False
        
    time.sleep(0)
    while tasks.empty():
        time.sleep(0)
        pass
        
