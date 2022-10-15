"""Small example OSC client

This program sends 10 random values between 0.0 and 1.0 to the /filter address,
waiting for 1 seconds between each value.
"""
import argparse
import random
import time
from tkinter.tix import Tree

from pythonosc import udp_client


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip", default="148.206.152.188",
      help="The ip of the OSC server")
  parser.add_argument("--port", type=int, default=5005,
      help="The port the OSC server is listening on")
  args = parser.parse_args()

  client = udp_client.SimpleUDPClient(args.ip, args.port)

  while True:
    client.send_message("/AF3", random.random())
    client.send_message("/T7", random.random())
    client.send_message("/Pz", random.random())
    client.send_message("/T8", random.random())
    client.send_message("/AF4", random.random())
    print(random.random())
    time.sleep(.001)
