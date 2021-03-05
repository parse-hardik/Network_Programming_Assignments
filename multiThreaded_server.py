import argparse, socket, time
from threading import Thread

tasks = {
    b'Beautiful is better than?' : b'Ugly.',
    b'Explicit is better than?' : b'Implicit.',
    b'What session?' : b'2020-2021.',
}

def create_socket(address):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(address)
    listener.listen(64)
    print('listening at {}'.format(address))
    return listener

def accept_forever(listener):
    while True:
        sock, address = listener.accept()
        print('Accepted connection from {}'.format(address))
        handle_conversation(sock,address)

def handle_conversation(sock, address):
    try:
        while True:
            handle_request(sock)
    except EOFError:
        print('Client socket to {} has closed'.format(address))
    except Exception as e:
        print('Client {} error {}'.format(address,e))
    finally:
        sock.close()

def handle_request(sock):
    task = recv_untill(sock,b'?')
    ans = get_ans(task)
    sock.sendall(ans)

def recv_untill(sock, suffix):
    msg = sock.recv(4096)
    if not msg:
        raise EOFError('socket closed')
    while not msg.endswith(suffix):
        data = sock.recv(4096)
        if not data:
            raise IOError('received {!r} then socket closed'.format(msg))
        msg+=data
    return msg

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

def start_threads(listener, workers=4):
    t = (listener,)
    for i in range(workers):
        Thread(target=accept_forever, args=t).start()

if __name__=='__main__':
    address = parse_cmd_line('Multi-Threaded server')
    listener = create_socket(address)
    start_threads(listener)