import asyncore
import socket

from Channel import Channel

class Server(asyncore.dispatcher):
	channelClass = Channel
	
	def __init__(self, channelClass=None, localaddr=("127.0.0.1", 31425), listeners=5):
		if channelClass:
			self.channelClass = channelClass
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind(localaddr)
		self.listen(listeners)
	
	def handle_accept(self):
		try:
			conn, addr = self.accept()
		except socket.error:
			print 'warning: server accept() threw an exception'
			return
		except TypeError:
			print 'warning: server accept() threw EWOULDBLOCK'
			return
		
		channel = self.channelClass(conn, addr, self)
		channel.Send({"action": "connected"})
		if hasattr(self, "Connected"):
			self.Connected(channel, addr)

#########################
#	Test stub	#
#########################

if __name__ == "__main__":
	class ServerChannel(Channel):
		def Action_hello(self, data):
			print "*Server* ran test method for 'hello' action"
			print "*Server* received:", data
	
	class EndPointChannel(Channel):
		def Connected(self):
			print "*EndPoint* Connected()"
		
		def Action_connected(self, data):
			print "*EndPoint* Action_connected(", data, ")"
			print "*EndPoint* initiating send"
			outgoing.Send({"action": "hello", "data": {"a": 321, "b": [2, 3, 4], "c": ["afw", "wafF", "aa", "weEEW", "w234r"], "d": ["x"] * 256}})
	
	def Connected(channel, addr):
		print "*Server* Connected() ", channel, "connected on", addr
	
	server = Server(channelClass=ServerChannel)
	server.Connected = Connected
	
	sender = asyncore.dispatcher()
	sender.create_socket(socket.AF_INET, socket.SOCK_STREAM)
	sender.connect(("localhost", 31425))
	outgoing = EndPointChannel(sender)
	
	from time import sleep
	
	print "*** polling for half a second"
	for x in range(50):
		asyncore.poll2()
		sleep(0.001)

