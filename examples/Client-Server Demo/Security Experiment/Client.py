import getpass
import sys
import _thread
import io_custom.c
import io_custom.aens_time
import io_custom.compress

DEBUG = False
OUTPUT = True

def main(host, port):
    global lock
    lock = _thread.allocate_lock()
    client = io_custom.c.Client()
    client.client.syncronize(True)
    # AUTHENTICATION
    client.client.install('novel.compression.procedure', io_custom.compress.encode)
    client.client.install('confirm.dream', io_custom.aens_time.format)
    client.client.install('welcome', lambda string: string)
    # I/O REDIRECTION
    client.client.install('io.stdout', sys.stdout)
    client.client.install('io.stderr', sys.stderr)
    client.client.install('io.stdin', sys.stdin)
    # EXIT CONTROL
    client.client.install('exit', lock.release)
    client.client.install('__repr__', lambda: 'Client Instance')
    client.client.connect(host, port)
    # ACTIVE ID CHECK
    authenticate(client)
    lock.acquire()
    lock.acquire()

def authenticate(client):
    more = True
    while more:
        username = input('Username: ')
        password = getpass.getpass()
        more = not client.name.code(username, password)
        if not more:
            break
        print('\nBad name or pass.\n')
    print('Success!')

################################################################################

if DEBUG:
    my_out = sys.stdout
    def new_thread(function, args, kwargs=None):
        if kwargs is None:
            org_thread(debug_thread, tuple([function] + list(args)))
        else:
            org_thread(debug_thread, tuple([function] + list(args)), kwargs)
    org_thread = _thread.start_new_thread
    _thread.start_new_thread = new_thread
    def debug_thread(*args, **kwargs):
        global _thread_id, _thread_count
        _thread_lock.acquire()
        _thread_id += 1
        _thread_count += 1
        ident = _thread_id
        my_out.write('Start Thread %s: %s(%s)\n' % (ident, args[0].__name__, ', '.join(map(repr, args[1:]))))
        my_out.write('%s threads active.\n\n' % _thread_count)
        _thread_lock.release()
        try:
            args[0](*args[1:], **kwargs)
        except SystemExit:
            pass
        except:
            traceback.print_exc()
        _thread_lock.acquire()
        _thread_count -= 1
        my_out.write('End Thread %s: %s(%s)\n' % (ident, args[0].__name__, ', '.join(map(repr, args[1:]))))
        my_out.write('%s threads active.\n\n' % _thread_count)
        _thread_lock.release()
    _thread_id    = 1
    _thread_count = 1
    _thread_lock  = _thread.allocate_lock()
    import traceback

################################################################################

if not OUTPUT:
    class dummy_file:
        def write(self, arg):
            pass
    sys.stdout = sys.stderr = dummy_file()

################################################################################

if __name__ == '__main__':
    main('127.0.0.1', 8080)
