import argparse, socket, time, select

tasks = {
    b'Beautiful is better than?' : b'Ugly.',
    b'Explicit is better than?' : b'Implicit.',
    b'What session?' : b'2020-2021.',
}

def all_events_forever(pollobj):
    while True:
        for fd, event in pollobj.poll():
            yield fd, event

def recv_until(sock, suffix):
    msg = sock.recv(4096)
    if not msg:
        raise EOFError('socket closed')
    while not msg.endswith(suffix):
        data = sock.recv(4096)
        if not data:
            raise IOError('received {!r} then socket closed'.format(msg))
        msg+=data
    return msg

def serve(listener):
    sockets = {listener.fileno(): listener}
    addresses = {}
    bytes_received = {}
    bytes_to_send = {}
    pollobj = select.poll()
    pollobj.register(listener, select.POLLIN)
    for fd, event in all_events_forever(pollobj):
        sock = sockets[fd]
        # If new connection comes
        if sock is listener:
            sock, address = sock.accept()
            print('Accepted connection from {}'.format(address))
            sock.setblocking(True)
            sockets[sock.fileno()] = sock
            addresses[sock] = address
            pollobj.register(sock, select.POLLIN)
        
        # Socket closed from client side
        elif event & (select.POLLHUP | select.POLLERR | select.POLLNVAL):
            address = addresses.pop(sock)
            rb = bytes_received.pop(sock, b'')
            sb = bytes_to_send.pop(sock, b'')
            if rb:
                print('Abnormal close, client {} sent {} but then closed'.format(address,rb))
            elif sb:
                print('Abnormal close, client {} closed before we sent {}'.format(address,sb))
            else:
                print('Normally closed by client {}'.format(address))
            pollobj.unregister(fd)
            del sockets[fd]

        # Server is ready to read
        elif event & select.POLLIN:
            more_data = sock.recv(4096)
            if not more_data:
                sock.close()
                continue
            data = bytes_received.pop(sock, b'') + more_data
            if data.endswith(b'?'):
                # bytes_to_send[sock] = data
                print('Question asked is {}'.format(data))
                if 'books' in data:
                    client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client1.connect(('localhost', 5000))
                    client1.sendall(data)
                    ans = recv_until(client1, b'.')
                    client1.close()
                else:
                    client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client2.connect(('localhost', 6000))
                    client2.sendall(data)
                    ans = recv_until(client2, b'.')
                    client2.close()
                bytes_to_send[sock] = ans
                pollobj.modify(sock, select.POLLOUT)
            else:
                bytes_received[sock] = data

        # Server is ready to send
        elif event & select.POLLOUT:
            data = bytes_to_send.pop(sock)
            n = sock.send(data)
            if n<len(data):
                bytes_to_send[sock] = data[n:]
            else:
                pollobj.modify(sock, select.POLLIN)

def create_socket(address):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(address)
    listener.listen(64)
    print('listening at {}'.format(address))
    return listener

def get_ans(task):
    time.sleep(2)
    return tasks.get(task, b'Error: Unknown task')

def parse_cmd_line(desc):
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('host', help='IP or hostname')
    parser.add_argument('-p', metavar='port', type=int, default=1060, help='TCP port')
    args = parser.parse_args()
    address = (args.host, args.p)
    return address

if __name__=='__main__':
    address = parse_cmd_line('Multi-Threaded server')
    listener = create_socket(address)
    serve(listener)