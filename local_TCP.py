import argparse
import socket
from datetime import datetime

MAX_BYTES = 65555

def recvall(sock, length):
	data = b''
	while len(data) < length:
		more = sock.recv(length-len(data))
		if not more:
			raise EOFError('was expecting %d bytes but only received' ' %d bytes before the socket closed' %(length,len(data)))
		data += more
	return data

def server(interface, port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind((interface, port))
	sock.listen(1)
	print('Listening at', sock.getsockname())
	while True:
		sc, sockname = sock.accept()
		print('We have received connection from ', sockname)
		print('Sock name: ', sc.getsockname())
		print('Sock peer: ', sc.getpeername())
		message = recvall(sc,16)
		print('Message is received')
		sc.sendall(b'Thank you client')
		sc.close()

def client(host, port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((host,port))
	print('Client has been assigned socket name ', sock.getsockname())
	sock.sendall(b'Hello server, we are using TCP protocol for communication')
	reply = recvall(sock,16)
	print('The server said\n\t', repr(reply))
	sock.close()

if __name__ == '__main__':
	choices = {'client': client, 'server': server}
	parser = argparse.ArgumentParser(description='Send and recieve TCP locally')
	parser.add_argument('role', choices=choices, help='which role to play')
	parser.add_argument('host', help='fjhfjhv')
	parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='UDP port (default 53)')
	args = parser.parse_args()
	function = choices[args.role]
	function(args.host, args.p)