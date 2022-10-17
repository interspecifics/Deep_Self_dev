"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
"""
import argparse
import keyboard
from datetime import datetime as dt

from pythonosc import dispatcher
from pythonosc import osc_server

def print_volume_handler(unused_addr, args, volume):
  print("[{0}] ~ {1}".format(args[0], volume))

def print_compute_handler(unused_addr, args, volume):
  try:
    print("[{0}] ~ {1}".format(args[0], args[1](volume)))
  except ValueError: pass

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip", default="127.0.0.1", help="The ip to listen on")
  parser.add_argument("--port", type=int, default=1234, help="The port to listen on")
  parser.add_argument("-u", "--user", default='', help="name of user being monitored")

  args = parser.parse_args()

  # creating csv
  user = vars(args)['user']
  if user:
      filename = "recordings/" + user + "_EEG " + str(dt.now())[:-7] + ".csv"
  else:
      filename = "recordings/EEG " + str(dt.now())[:-7] + ".csv"
  filename = filename.replace(' ', '_').replace(':','')
  with open(filename, 'w') as f:
      f.write("counter,AF3,T7,Pz,T8,AF4,key\n")

  dispatcher = dispatcher.Dispatcher()
  f = open(filename, 'a')

  def write_line(aux, str_line):
      # if keyboard.is_pressed('k'):
      #   f.write(str_line + "k,\n")
      # else:
      f.write(str_line + ",\n")
      if keyboard.is_pressed('c'):
        f.close()
              
  dispatcher.map("/eeg_line", write_line)

  server = osc_server.ThreadingOSCUDPServer(
      (args.ip, args.port), dispatcher)
  print("Serving on {}".format(server.server_address))
  server.serve_forever()