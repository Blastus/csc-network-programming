#! /usr/bin/env python3
import collections
import socket
import threading
import select

def main():
    server = Server(Address(socket.gethostname(), 8080),
                    Address(socket.gethostname(), 80))
    server.start()
    server.join()

Address = collections.namedtuple('Address', 'host, port')

class Server(threading.Thread):

    def __init__(self, bind_address, remote_address):
        super().__init__()
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.bind(bind_address)
        self.__remote_address = remote_address

    def run(self):
        self.__server.listen(5)
        while True:
            client, address = self.__server.accept()
            print('Server connection:', address, flush=True)
            Proxy(self.__remote_address, client).start()

class Proxy(threading.Thread):

    def __init__(self, remote_address, client):
        super().__init__()
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.connect(remote_address)
        self.__client = client

    def run(self):
        pairs = {self.__server: self.__client, self.__client: self.__server}
        while True:
            read, write, error = select.select(pairs.keys(), pairs.keys(), ())
            print('Proxy select', flush=True)
            for source in read:
                destination = pairs[source]
                if destination in write:
                    destination.sendall(source.recv(1 << 12))

if __name__ == '__main__':
    main()
