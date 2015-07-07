#! /usr/bin/env python3
import time
import socket
import traceback
import tkinter
import tkinter.font

ADDRESS = '4dwebservices.pcci.int', 8001
TIMEOUT = 5

def main():
    while True:
        print(time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
        try:
            client = socket.create_connection(ADDRESS, TIMEOUT)
        except:
            # Show error information.
            print()
            traceback.print_exc()
            print()
            # Show GUI error message.
            root = tkinter.Tk()
            root.resizable(False, False)
            root.title('Service Monitor')
            font = tkinter.font.Font(family='Arial Black', size=72)
            note = tkinter.Label(text='Server is down!', font=font)
            note.grid()
            tkinter.mainloop()
        else:
            client.shutdown(socket.SHUT_RDWR)
            client.close()
            time.sleep(TIMEOUT)

if __name__ == '__main__':
    main()
