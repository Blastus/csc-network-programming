#! /usr/bin/env python3
"""Module for simple UDP broadcast support.

The classes in this module are stepping stones for building discoverable
services on a network. Server replies are to be handled by the importer."""

################################################################################

__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'
__date__ = '6 July 2015'
__version__ = '$Revision: 2 $'

################################################################################

import socket
import _thread
import time

################################################################################

class Client:

    "Client(port) -> Client instance"

    __slots__ = '__socket', '__address'

    def __init__(self, port):
        "Initialize the client with a sending socket."
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
        self.__address = '255.255.255.255', port

    def connect(self, data):
        "Send a broadcast through the underlying socket."
        self.__socket.sendto(data, self.__address)

################################################################################

class Server:

    "Server(port) -> Server instance"

    __slots__ = '__socket'

    def __init__(self, port):
        "Initialize the server with a receiving socket."
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.__socket.bind(('0.0.0.0', port))

    def accept(self, size):
        "Receive a broadcast through the underlying socket."
        return self.__socket.recvfrom(size)
