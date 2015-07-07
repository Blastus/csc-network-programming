import os
from . import laboratory_test
from .laboratory_test import *

################################################################################

def loop():
    valid_disk = False
    while True:
        print()
        print('PROGRAM MENU')
        print('============')
        print('(1) Create Disk')
        print('(2) Load Disk')
        if valid_disk:
            print('(3) Save Disk')
            print('(4) Use Disk')
        while True:
            try:
                select = input('Select: ')
            except:
                exit(0)
            try:
                select = int(select)
                if 0 < select < 3 or (2 < select < 5 and valid_disk):
                    break
                else:
                    print('Select should be between 1 and', end=' ')
                    if valid_disk:
                        print('4.')
                    else:
                        print('2.')
            except:
                print('Select should be a number.')
            print()
        if select == 1:
            disk = create_disk()
            disk.seed(False)
            valid_disk = True
        elif select == 2:
            disk = load_disk()
            if disk is not None:
                disk.seed(False)
                valid_disk = True
        elif select == 3:
            save_disk(disk)
        else:
            use_disk(disk)

laboratory_test.loop = loop

################################################################################

def load_disk():
    while True:
        try:
            print()
            print('LOAD A DISK')
            name = input('FILENAME: ')
            disk = DAL6(10, 10)
            disk.load(name, False)
            return disk
        except EOFError:
            return
        except:
            print('INVALID FILENAME')

laboratory_test.load_disk = load_disk

################################################################################

class Shell(laboratory_test.Shell):

    # The Users Interface
    def __init__(self, context):
        assert context.__class__ is Context
        self.__context = context
        self.__commands = ['chdir', 'getcwd', 'listdir', \
                           'mkdir', 'rmdir', 'remove', 'exit']
        self.__programs = ['type', 'edit', 'import']
        print('Welcome to DAL')
        print('==============')
        while True:
            try:
                prompt = input('>>> ')
            except:
                continue
            if prompt == 'help':
                print('COMMANDS:')
                print('  chdir: change current working directory')
                print('  getcwd: get current working directory')
                print('  listdir: display directory contents')
                print('  mkdir: make a new directory')
                print('  rmdir: remove an old directory')
                print('  remove: remove a file')
                print('  exit: terminates this shell')
                print('PROGRAMS:')
                print('  type: display the contents of a file')
                print('  edit: create a new file')
                print('  import: copy file system into program')
            else:
                prompt = prompt.split(' ')
                command = prompt[0]
                path = ' '.join(prompt[1:])
                if command in self.__commands:
                    if command == 'chdir':
                        self.__chdir(path)
                    elif command == 'getcwd':
                        self.__getcwd()
                    elif command == 'listdir':
                        self.__listdir(path)
                    elif command == 'mkdir':
                        self.__mkdir(path)
                    elif command == 'rmdir':
                        self.__rmdir(path)
                    elif command == 'remove':
                        self.__remove(path)
                    else:
                        break
                elif command in self.__programs:
                    if command == 'type':
                        try:
                            Type(self.__context, path)
                        except:
                            print('Type has crashed.')
                    elif command == 'edit':
                        try:
                            Edit(self.__context, path)
                        except:
                            print('Edit has crashed.')
                    elif command == 'import':
                        try:
                            Import(self.__context, path)
                        except:
                            print('Import has crashed.')
                    else:
                        break
                else:
                    print(repr(command), 'is an unrecognized command or program.')

laboratory_test.Shell = Shell

################################################################################

class Import:

    # Import File System
    def __init__(self, context, path):
        assert isinstance(context, Context) and isinstance(path, str)
        self.con = context
        while True:
            try:
                fold = input('Directory: ')
                if os.path.isdir(fold):
                    self.__engine(fold)
                    break
                else:
                    print('PATH IS NOT A DIRECTORY')
            except AssertionError:
                print('PATH ALREADY EXISTS')
            except:
                break

    # COPY THE FOLDER
    def __engine(self, fold):
        cwd = self.con.getcwd()
        basename = '. ' + os.path.basename(fold).replace(' ', '_')
        assert not self.con.exists(basename)
        self.con.mkdir(basename)
        self.con.chdir(basename)
        try:
            for name in os.listdir(fold):
                path = os.path.join(fold, name)
                try:
                    if os.path.isdir(path):
                        self.__engine(path)
                    elif os.path.isfile(path):
                        data = file(path, 'rb').read()
                        new_file = self.con.file('. ' + name.replace(' ', '_'), 'w')
                        new_file.write(data)
                        new_file.close(True)
                except:
                    pass
        except:
            pass
        self.con.chdir(cwd)
