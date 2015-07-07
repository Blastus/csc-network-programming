#! /usr/bin/env python3
'''Module for running simple proxies.

This module provides a single class that can build
proxy objects capable of being started and stopped.'''

################################################################################

__version__ = '$Revision: 1 $'
__date__ = 'July 6, 2015'
__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'
__credits__ = '''\
S. Schaub, for introducing me to programming.
S. Sechrest, for writing an introductory tutorial.
S. Leffler, for authoring a more advanced tutorial.'''

################################################################################

import select as _select
import socket as _socket
import sys as _sys
import _thread

################################################################################

class Proxy:

    'Proxy(bind, connect) -> Proxy'

    FAMILY = _socket.AF_INET
    TYPE = _socket.SOCK_STREAM
    BUFFERSIZE = 1 << 12

    def __init__(self, bind, connect):
        'Initialize the Proxy object.'
        self.__bind = bind
        self.__connect = connect
        self.__active = False
        self.__thread = False
        self.__lock = _thread.allocate_lock()

    def start(self):
        'Start the Proxy object.'
        self.__lock.acquire()
        self.__active = True
        if not self.__thread:
            self.__thread = True
            _thread.start_new_thread(self.__proxy, ())
        self.__lock.release()

    def stop(self):
        'Stop the Proxy object.'
        self.__lock.acquire()
        self.__active = False
        self.__lock.release()

    def __proxy(self):
        'Private class method.'
        proxy = _socket.socket(self.FAMILY, self.TYPE)
        proxy.bind(self.__bind)
        proxy.listen(5)
        while True:
            client = proxy.accept()[0]
            self.__lock.acquire()
            if not self.__active:
                proxy.close()
                client.shutdown(_socket.SHUT_RDWR)
                client.close()
                self.__thread = False
                self.__lock.release()
                break
            self.__lock.release()
            server = _socket.socket(self.FAMILY, self.TYPE)
            server.connect(self.__connect)
            _thread.start_new_thread(self.__serve, (client, server))

    def __serve(self, client, server):
        'Private class method.'
        pairs = {client: server, server: client}
        while pairs:
            for socket in _select.select(list(pairs.keys()), [], [])[0]:
                buffer = socket.recv(self.BUFFERSIZE)
                if buffer:
                    pairs[socket].sendall(buffer)
                else:
                    pairs[socket].shutdown(_socket.SHUT_WR)
                    socket.shutdown(_socket.SHUT_RD)
                    del pairs[socket]
        client.close()
        server.close()
