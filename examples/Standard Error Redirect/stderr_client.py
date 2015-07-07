ADDR = 'localhost', 8090

import socket, sys, atexit

client = socket.socket()
client.connect(ADDR)
file = sys.stderr = client.makefile('w')

def close(stream, client_socket, how):
    stream.flush()
    client_socket.shutdown(how)
    client_socket.close()

atexit.register(close, file, client, socket.SHUT_RDWR)
