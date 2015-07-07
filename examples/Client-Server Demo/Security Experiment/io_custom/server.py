import atexit, sys, time, _thread, getpass, traceback
import builtins
from . import s, compress, aens_time

THREAD_DATA = False

PASSCODE = '''\
"ApPlE" is an example of a good PASSCODE.
However, the first string used was not in
a compressable state. That is why the new
string is much longer. You may change the
PASSCODE that you find here if it needs a
different look to itself. The results can
be slightly different with small changes.'''

def enable(host, port, ID_database, programs):
    global p, ID, org_thread
    # GLOBALS
    p = programs
    org_thread = _thread.start_new_thread
    _thread.start_new_thread = new_thread
    ID = dict([(item[0].lower(), item[1]) for item in list(ID_database.items())])
    # OVER-RIDE OUTPUT
    sys.stdout = IO_Manager(sys.stdout)
    sys.stderr = IO_Manager(sys.stderr)
    sys.stdin = IO_Manager(sys.stdin)
    # SERVER
    server = s.Server(connection)
    # authentication and option control
    server.install('name.code', autostart)
    server.with_client('name.code')
    server.install('__repr__', lambda: 'Server Instance')
    # self documentation
    server.title('PROGRAM SERVER')
    server.name("%s's Server" % getpass.getuser())
    server.documentation('''\
    The purpose of this server is to provide
    remote, multi-user access to various programs
    that are installed on this server. This server
    will automatically authenticate clients. If
    your client has automatically authenticated
    itself, you should log in with the "name.code"
    procedure. Be sure to have "io.stdout.write,"
    "io.stderr.write," and "io.stdin.readline"
    methods installed on your client before doing
    so. Once logged in, this server will take
    control of your I/O, provide a menu, and give
    you an opportunity to run one of the installed
    programs. For further information, please
    contact my administrator.''')
    server.start(host, port)
    # LOCK THIS THREAD
    lock = _thread.allocate_lock()
    lock.acquire()
    lock.acquire()

def new_thread(function, args, kwargs=None):
    args = tuple([_thread.get_ident(), function] + list(args))
    if kwargs is None:
        org_thread(io_thread_start, args)
    else:
        org_thread(io_thread_start, args, kwargs)

if THREAD_DATA:
    _thread_id    = 1                       # THREAD ID
    _thread_count = 1                       # THREAD COUNT
    _thread_lock  = _thread.allocate_lock()  # NUMBER LOCK
    def io_thread_start(*args, **kwargs):   # THREAD TESTER
        global _thread_id, _thread_count
        # Test Code
        _thread_lock.acquire()
        _thread_id += 1
        _thread_count += 1
        ident = _thread_id
        sys.stdout.write('Start Thread %s: %s(%s)\n' % (ident, args[1].__name__, ', '.join(map(repr, args[2:]))))
        sys.stdout.write('%s threads active.\n\n' % _thread_count)
        _thread_lock.release()
        # Main Code
        sys.stdout.add(args[0])
        sys.stderr.add(args[0])
        sys.stdin.add(args[0])
        safestart(args[1], *args[2:], **kwargs)
        sys.stdout.rm_client()
        sys.stderr.rm_client()
        sys.stdin.rm_client()
        # Test Code
        _thread_lock.acquire()
        _thread_count -= 1
        sys.stdout.write('End Thread %s: %s(%s)\n' % (ident, args[1].__name__, ', '.join(map(repr, args[2:]))))
        sys.stdout.write('%s threads active.\n\n' % _thread_count)
        _thread_lock.release()
else:
    def io_thread_start(*args, **kwargs):
        sys.stdout.add(args[0])
        sys.stderr.add(args[0])
        sys.stdin.add(args[0])
        safestart(args[1], *args[2:], **kwargs)
        sys.stdout.rm_client()
        sys.stderr.rm_client()
        sys.stdin.rm_client()

def autostart(client, name, password):
    if verify(name, password):
        _thread.start_new_thread(start, (client,))
        return True
    return False

def verify(name, password):
    name = name.lower()
    if name in ID:
        return ID[name] == password
    return False

def connection(client):
    # AUTHENTICATION
    try:
        client.client.timeout(1)
        # COMPRESSION
        part1, part2 = client.novel.compression.procedure(PASSCODE)
        string, key = compress.encode(PASSCODE)
        assert part1 == string
        assert part2 == key
        # OTHER WORLD
        seconds = aens_time.seconds()
        string = client.confirm.dream(seconds)
        assert string == aens_time.format(seconds)
        # HELLO THERE
        assert client.welcome('ID OK\nGreetings!').startswith('ID OK\n')
        client.client.clear()
    except:
        client.client.end()
        print('''\n\n\n\n\n\n
        =====================
        AUTHENTICATION FAILED
        =====================
        \n\n\n\n\n\n\n\n\n''')

def time_it(function, *arg, **kw): # TEST
    t = time.time()
    data = function(*arg, **kw)
    print('Time: ' + str(time.time() - t))
    return data

def start(client):
    time.sleep(1)
    # I/O REDIRECT
    sys.stdout.add(client.io.stdout.write)
    sys.stderr.add(client.io.stderr.write)
    sys.stdin.add(client.io.stdin.readline)
    # PROGRAM EXECUTION
    safestart(menu, p)
    # I/O DISCONNECT
    sys.stdout.rm_client()
    sys.stderr.rm_client()
    sys.stdin.rm_client()
    # PROGRAM EXIT
    client.exit()
    time.sleep(0.1)

def safestart(function, *arg, **kw):
    try:
        function(*arg, **kw)
    except SystemExit:
        pass
    except:
        traceback.print_exc()

def menu(programs):
    print('PLEASE SELECT A PROGRAM')
    for index, name in [(x[0] + 1, x[1]) for x in enumerate(sorted(programs.keys()))]:
        print('(%s) %s' % (index, name))
    while True:
        try:
            i = int(input('Selection: ')) - 1
            assert 0 <= i < len(programs)
            key = sorted(programs.keys())[i]
            break
        except EOFError:
            return
        except:
            print('PLEASE SELECT A PROGRAM')
    func, arg, kw = programs[key]
    safestart(func, *arg, **kw)

################################################################################

class IO_Manager:

    def __init__(self, default):
        self.__std = default
        self.__map = {}
        self.__mtx = _thread.allocate_lock()

    def add(self, stream):
        ident = _thread.get_ident()
        self.__mtx.acquire()
        if isinstance(stream, int):
            if stream in self.__map:
                self.__map[ident] = self.__map[stream]
        else:
            self.__map[ident] = stream
        self.__mtx.release()

    def rm_client(self):
        ident = _thread.get_ident()
        self.__mtx.acquire()
        if ident in self.__map:
            del self.__map[ident]
        self.__mtx.release()

    def write(self, data):
        ident = _thread.get_ident()
        self.__mtx.acquire()
        if ident in self.__map:
            client = True
            key = self.__map[ident]
        else:
            client = False
        self.__mtx.release()
        if client:
            key(data)
        else:
            self.__std.write(data)

    def readline(self):
        ident = _thread.get_ident()
        self.__mtx.acquire()
        if ident in self.__map:
            client = True
            key = self.__map[ident]
        else:
            client = False
        self.__mtx.release()
        if client:
            return key()
        else:
            return self.__std.readline()
