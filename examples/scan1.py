#! /usr/bin/env python3
import os
import sys
import socket
import _thread

def main(argv):
    if len(argv) == 2:
        host = argv[1]
        if valid(host):
            scan(host)
            return
    print('Usage: {} <host>'.format(os.path.basename(argv[0])))

def valid(host):
    try:
        socket.gethostbyname(host)
    except socket.gaierror:
        return False
    else:
        return True

def scan(host):
    mutex = _thread.allocate_lock()
    compare = _thread.allocate_lock()
    mutex.acquire()
    numbers = []
    for port in range(1 << 16):
        _thread.start_new_thread(test, (host, port, numbers, mutex, compare))
    mutex.acquire()
    print('Ports:', *filter(None, numbers))

def test(host, port, numbers, mutex, compare):
    sock = socket.socket()
    try:
        sock.connect((host, port))
    except socket.error:
        compare.acquire()
        numbers.append(None)
    else:
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        compare.acquire()
        numbers.append(port)
    release = len(numbers) == 1 << 16
    compare.release()
    if release:
        mutex.release()

if __name__ == '__main__':
    main(sys.argv)
