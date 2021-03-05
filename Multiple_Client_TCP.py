import argparse
import socket
import time
import random
from datetime import datetime

tasks = {b'Beautiful is better than?': b'Ugly.',
         b'Explicit is better than?': b'Implicit.',
         b'What session?': b'2020-2021.'}


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


def client(host, port):
    print("Hello\n")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # print(sock)
    sock.connect((host, port))
    print('Client has been assigned socket name ', sock.getsockname())
    for task in random.sample(list(tasks), 3):
        sock.sendall(task)
        ans = recv_until(sock, b'.')
        print(ans)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print('current time is ', current_time)
    sock.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send and recieve TCP locally')
    # parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='fjhfjhv')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='UDP port (default 53)')
    args = parser.parse_args()
    # function = choices[args.role]
    client(args.host, args.p)
