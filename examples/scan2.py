#! /usr/bin/env python3
import sys
import socket
import os
import _thread

################################################################################

def main():
    "Checks the command line for a host and tries to scan its ports."
    if len(sys.argv) == 2:
        try:
            host = socket.gethostbyname(sys.argv[1])
        except socket.gaierror:
            pass
        else:
            return scan(host)
    print('Usage: {} <host>'.format(os.path.basename(sys.argv[0])))

def scan(host):
    "Creates a thread for each port and shows valid connections."
    valid = []
    mutex = _thread.allocate_lock()
    sleep = _thread.allocate_lock()
    sleep.acquire()
    for port in range(1 << 16):
        _thread.start_new_thread(test, (host, port, valid, mutex, sleep))
    sleep.acquire()
    print('Ports: ' + ', '.join(map(str, sorted(filter(None, valid)))))

def test(host, port, valid, mutex, sleep):
    "Connects to given address and reports success or failure on port."
    client = socket.socket()
    try:
        client.connect((host, port))
    except socket.error:
        mutex.acquire()
        valid.append(None)
    else:
        client.shutdown(socket.SHUT_RDWR)
        client.close()
        mutex.acquire()
        valid.append(port)
    done = len(valid) == 1 << 16
    mutex.release()
    if done:
        sleep.release()

################################################################################

if __name__ == '__main__':
    main()
