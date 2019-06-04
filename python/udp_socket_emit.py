import socket

class udp_emit:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect((host, port))
        
    def emit(self, data):
        try:
            self.sock.sendall(data)
        except:
            pass
            #uncomment if you want to be notified
            #print("cannot send data over udp socket, the destination is either not listening yet or is refusing to connect.  Check to see if it's running yet.")
