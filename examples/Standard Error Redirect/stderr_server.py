ADDR = '', 8090

import socket

server = socket.socket()
server.bind(ADDR)
server.listen(1)

while True:
    client = server.accept()[0]
    message = ''
    while True:
        buffer = client.recv(1 << 12)
        if buffer:
            message += buffer.decode()
        else:
            print(message)
            break
