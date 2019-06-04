from argparse import ArgumentParser

from controller_values import daydream_bluetooth
from udp_socket_emit import udp_emit
from udev_evdev_emit import udev_evdev_emit

def main():
    emitclass = None
    
    #command line arguments
    parser = ArgumentParser()
    
    #-h can't be used because it's reserved to mean help
    parser.add_argument("-t", "--host", dest="host", default=None,
                        help="host to use, eg 127.0.0.1")
    parser.add_argument("-p", "--port",
                        dest="port", default=None, type=int,
                        help="port to use")

    parser.add_argument("-u", "--udev", help="use this option to use a udev emit approach", type=bool, dest="udev")
    
    args = parser.parse_args()    
    HOST = args.host
    PORT = args.port
    
    if args.udev:
        emitclass = udev_evdev_emit()
    elif HOST and PORT:
        emitclass = udp_emit(HOST, PORT)
    
    bluecontroller = daydream_bluetooth()
    bluecontroller.emitclass = emitclass
    bluecontroller.run()
  

if __name__ == '__main__':
    main()
