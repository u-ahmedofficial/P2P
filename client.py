
import socket
import threading
import sys
import time
from random import randint
import os

class Client:
	

	def sendMsg(self, sock):
		while True:
			print("All Chunks Recieved And Reassembled in file: received_file.jpg")
			sock.send(bytes(input(""),"utf_8"))

	def __init__(self,address):
		sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #same as server
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#same as server
		sock.connect((address,10000)) #connecting to server
		iThread=threading.Thread(target=self.sendMsg, args=(sock,))
		iThread.daemon=True
		iThread.start()


		total=0
		f=open('received_file.jpg', 'wb') #recieving file from server
		while True:
			data =sock.recv(1024)
			if not data:break
			else:
				f.write(data) #writing data of all chunks to file....
		print("All Chunks Recieved And Reassembled in file: received_file.jpg")	