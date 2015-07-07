#! /usr/bin/env python3
import select
import socket
import _thread
import time

################################################################################

BIND = '', 8010
CONNECT = 'localhost', 8080

################################################################################

class Proxy:

    "Proxy(bind, connect) -> Proxy"

    FAMILY = socket.AF_INET
    TYPE = socket.SOCK_STREAM
    BUFFERSIZE = 1 << 12

    def __init__(self, bind, connect):
        "Initialize the Proxy object."
        self.__bind = bind
        self.__connect = connect
        self.__status = False
        self.__thread = False
        self.__lock = _thread.allocate_lock()

    def start(self):
        "Start the Proxy object."
        self.__lock.acquire()
        self.__status = True
        if not self.__thread:
            self.__thread = True
            _thread.start_new_thread(self.__proxy, ())
        self.__lock.release()

    def stop(self):
        "Stop the Proxy object."
        self.__lock.acquire()
        self.__status = False
        self.__lock.release()

    def __proxy(self):
        "Private class method."
        proxy = socket.socket(self.FAMILY, self.TYPE)
        proxy.bind(self.__bind)
        proxy.listen(5)
        while True:
            client = proxy.accept()[0]
            self.__lock.acquire()
            if not self.__status:
                proxy.close()
                self.__thread = False
                self.__lock.release()
                break
            self.__lock.release()
            server = socket.socket(self.FAMILY, self.TYPE)
            server.connect(self.__connect)
            _thread.start_new_thread(self.__serve, (client, server))

    def __serve(self, client, server):
        "Private class method."
        with open(str(time.time()) + '.txt', 'w') as file:
            pairs = {client: server, server: client}
            while pairs:
                read = select.select(pairs.keys(), [], [])[0]
                for sock in read:
                    string = sock.recv(self.BUFFERSIZE)
                    if string:
                        pairs[sock].sendall(string)
                        args = (sock.getsockname(),
                                sock.getpeername(),
                                time.ctime(), string)
                        print('{} -> {} at {}\n{}\n'.format(*args),
                              file=file)
                    else:
                        pairs[sock].shutdown(socket.SHUT_WR)
                        sock.shutdown(socket.SHUT_RD)
                        del pairs[sock]
            client.close()
            server.close()

################################################################################

def main():
    lock = _thread.allocate_lock()
    lock.acquire()
    proxy = Proxy(BIND, CONNECT)
    proxy.start()
    lock.acquire()

################################################################################

if __name__ == '__main__':
    main()
