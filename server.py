import socket
import threading
import sys
import time
from random import randint
import os

class Server:

	connections=[]
	peers=[]
	def __init__(self):
		sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Shows Family of socket, socket type TCP/UDP
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # for reusing the socket in case server disconnects so that peer takeover server socket
		sock.bind(('0.0.0.0',10000))
		sock.listen(5)
		print("Server Running...")
		while True:
			c,a=sock.accept()# C Conecting client ref object, A (ip,port)
			cThread=threading.Thread(target=self.handler,args=(c,a)) #Thread is used to make the code run at backend
			cThread.daemon=True # making thread daemon means we dont need to quit it 
			cThread.start()	
			self.connections.append(c) #add connection ref to the list after every peer connect
			self.peers.append(a[0])#add new peer to the list of peers
			print("{} : {} connected".format(str(a[0]),str(a[1])))

			
			self.split("pic.jpg",os.getcwd()+"/store/",250000) #spliting file
			try:
				self.sendFile(c) #sending file
			except:
				print("Exception in server")
			
	def handler(self,c,a):
		
		while True:
			data=c.recv(1024) #if client disconnects it sends fin sign
			for connection in self.connections: #notifying all
				connection.send(data) 
			if not data:break
			print("{} : {} disconnected".format(str(a[0]),str(a[1]))) #message on screen
			self.connections.remove(c)#removing that client from  connections list 
			self.peers.remove(a[0])#removing that client/peer from peers list
			c.close()#closing connection to that client/peer
			


	def split(self,fromfile, todir, chunksize): 
		if not os.path.exists(todir):                  # caller handles errors
			os.mkdir(todir)                            # make dir, read/write parts
		else:
			for fname in os.listdir(todir):            # delete any existing files
				os.remove(os.path.join(todir, fname)) 
			partnum = 0
			input1 = open(fromfile, 'rb')                   # use binary mode on Windows
			while True:                                       # eof=empty string from read
				chunk = input1.read(chunksize)              # get next part <= chunksize
				if not chunk: break
				partnum  = partnum+1
				filename = os.path.join(todir, ('part{:04}'.format(partnum)))
				fileobj  = open(filename, 'wb')
				fileobj.write(chunk)
				fileobj.close()                            # or simply open(  ).write(  )
			input1.close()

		assert partnum <= 9999                         # join sort fails if 5 digits
		print("File Splitting Done !!")
		print("Chunks are :")
		print(os.listdir(todir))


	def  sendFile(self,c):
		parts  = os.listdir(os.getcwd()+"/store/") #list directory to see files e.g part0001.jpg,part0002.jpg....
		parts.sort()#sorting the parts as 0001,0002 ....
		for filename in parts:
			filepath = os.path.join(os.getcwd()+"/store/", filename)#joining path with file like /root/python/P2P/part0001.jpg....
			fileobj  = open(filepath, 'rb')#writing to that path like root/python/P2P/part0001.jpg....
			while 1:
				filebytes = fileobj.read(250000) #reading data from chunks in order part1,part2....
				if not filebytes: break
				c.send(filebytes)#send chunks....
			fileobj.close()	
		print("Sent All Chunks !!!")

