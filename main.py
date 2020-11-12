import socket
import threading
import sys
import time
from random import randint
import os
from server import Server
from client import Client
from p2p import p2p
def main():
	while True:
		try:
			print("Starting Peer to Peer System ..... !!!")
			print("Trying to Connect....")
			time.sleep(randint(1,5))#Wait for Server to be ready
			for peer in p2p.peers:
				try:
					client=Client(peer) #connect the peer to all the peers+server previously connected
				except KeyboardInterrupt:
					sys.exit(0)
				except:
					pass

				try:
					server=Server() #if no peer then run the server
				except KeyboardInterrupt:
					sys.exit(0)
				except Exception as e:
					print(e)
				
		except KeyboardInterrupt:
			sys.exit(0)
if __name__ == '__main__':main()

	