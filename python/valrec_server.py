import socketserver
from argparse import ArgumentParser

class MyUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print(self.request[0])
        #self.data = self.request.recv(1024).strip()
        #print("() wrote:".format(self.client_address[0]))
        #print(self.data)
        
        
if __name__ == "__main__":
    #command line arguments
    parser = ArgumentParser()
    
    #-h can't be used because it's reserved to mean help
    parser.add_argument("-t", "--host", dest="host", default=None,
                        help="host to use, eg 127.0.0.1")
    parser.add_argument("-p", "--port",
                        dest="port", default=None, type=int,
                        help="port to use")

    args = parser.parse_args()    
    HOST = args.host
    PORT = args.port
    
    server = socketserver.UDPServer((HOST, PORT), MyUDPHandler)
    
    server.serve_forever()
