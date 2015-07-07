#! /usr/bin/env python3

import broadcast

TEMPLATE = 'From: {1}\nPort: {2}\nData: {0}\n'

def main(port):
    broadcast_server = broadcast.Server(port)
    while True:
        data, address = broadcast_server.accept(1 << 12)
        print(TEMPLATE.format(data.decode(), *address))

if __name__ == '__main__':
    main(50000)
