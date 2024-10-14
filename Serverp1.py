import socket
import threading
import datetime
import os

cached_responses = {}  # Dictionary to store cached responses
cache_timeout = 120  # Maximum age of cache in seconds
cache_dir = '/Users/sunny/Desktop/Cache'  # Directory to store cached responses


class Request_handler(threading.Thread):
    def __init__(self, client, server, proxy_port, thread_id, time):
        super(Request_handler, self).__init__()
        self.client = client
        self.server = server
        self.proxy_port = proxy_port
        self.thread_id = thread_id
        self.time= time

    def run(self):
        try:
            while True:
                
                data = self.client.recv(1024)
                filename=data.split()[1]
            #host_name=data.split()[1].split('/')[2]
                time_req=datetime.datetime.now()
                server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server.connect(self.server)
                if filename in cached_responses:
                    cached_timestamp = cached_responses[filename][1]
                    if time_req - cached_timestamp < cache_timeout:
                        print('proxy-cache, client, '+str(self.thread_id)+" "+str(self.time))
                        f=open(cache_dir +filename, 'rb')
                        outputdata=f.read()
                        self.client.send("HTTP/1.1 200 OK\r\n".encode())
                        self.client.send("Content-Type: text/html\r\n".encode())
                        self.client.send(data.encode())
                        for i in range(0, len(outputdata)):
                            self.client.send(outputdata[i].encode())
                        self.client.send("\r\n".encode())
                    break
        
                else:    
                    data_rcv = server.recv(1024)
                    data_rcv=data_rcv.decode()
                    print ('proxy-forward, client, '+str(self.thread_id)+" "+str(self.time))
                    self.client.send("HTTP/1.1 200 OK\r\n".encode())
                    self.client.send("Content-Type: text/html\r\n".encode())
                    self.client.send(data)
                    for i in range(0, len(data_rcv)):
                        self.client.sendall(data_rcv[i].encode())
                    self.client.send("\r\n".encode())
                    cached_responses[filename] = [time_req]
                    if not os.path.exists(cache_dir):
                        os.makedirs(cache_dir)
                    with open(cache_dir + filename, 'wb') as f:
                        f.write(data_rcv)
                server.close()
                break            
        finally:
            self.client.close()

class Proxy(threading.Thread):
    def __init__(self, port):
        super(Proxy, self).__init__()
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('localhost', self.port))
        self.server.listen(50)
        self.thread_counter = 0
        self.timestamp_counter = 0

    def get_thread_id(self):
        self.thread_counter += 1
        return self.thread_counter

    def get_timestamp(self):
        self.timestamp_counter= datetime.datetime.now()
        return self.timestamp_counter

    def run(self):
        while True:
            (client, client_address) = self.server.accept()
            thread_id = self.get_thread_id()
            time = self.get_timestamp()
            Request_handler = Request_handler(client, ('localhost', 1234), self.port, thread_id, time)
            Request_handler.start()

if __name__ == '__main__':
    proxy_server = Proxy(8081)
    proxy_server.start()
    print("start")
