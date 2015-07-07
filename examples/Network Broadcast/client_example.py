#! /usr/bin/env python3

import time
import broadcast

TEMPLATE = '%Y-%m-%dT%H:%M:%SZ'

def main(port):
    broadcast_client = broadcast.Client(port)
    while True:
        message = time.strftime(TEMPLATE, time.gmtime())
        broadcast_client.connect(message.encode())
        time.sleep(1)

if __name__ == '__main__':
    main(50000)
