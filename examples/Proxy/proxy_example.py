import os, proxy, sys, _thread

if not os.path.exists('proxy.ini'): open('proxy.ini', 'w').write('''localhost 80 8080\n127.0.0.1 80 9090 <server_name> <server_port> <proxy_port> <optional_text>''')

################################################################################

def main(setup, error):
    sys.stderr = open(error, 'a')
    for line in open(setup):
        parts = line.split()
        proxy.Proxy(('', int(parts[2])), (parts[0], int(parts[1]))).start()
    lock = _thread.allocate_lock()
    lock.acquire()
    lock.acquire()

################################################################################

if __name__ == '__main__':
    main('proxy.ini', 'error.log')
