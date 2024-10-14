import socket
import threading
import datetime
import os
import time

cached_responses = {}  
cache_timeout = 120  
cache_dir = '/Users/sunny/Desktop/Cache/' 
class HandleClient(threading.Thread):
    def __init__(self, client_socket, server_address, proxy_port, thread_id, timestamp):
        super(HandleClient, self).__init__()
        self.client_socket = client_socket
        self.server_address = server_address
        self.proxy_port = proxy_port
        self.thread_id = thread_id
        self.timestamp = timestamp

    def run(self):
        try:
            while True:
                data = self.client_socket.recv(1024).decode()
                #print(len(data.split('\n')))
                #print(data.split(''))
                filename=data.split(' ')[1]
                #print(filename)
                host_name=data.split('\n')[1]
                print(host_name)
                time_req=time.time()
                server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server.connect(self.server_address)
                print ('proxy-forward, server, '+str(self.thread_id)+" "+str(self.timestamp))
                server.sendall(data.encode())
                if filename in cached_responses:
                    cached_timestamp = cached_responses[filename][1]
                    if time_req - cached_timestamp < cache_timeout:
                        print('proxy-cache, client, '+str(self.thread_id)+" "+str(self.timestamp))
                        f=open(cache_dir + filename, 'r')
                        outputdata=f.read()
                        self.client_socket.send("HTTP/1.1 200 OK\r\n".encode())
                        self.client_socket.send("Content-Type: text/html\r\n".encode())
                        self.client_socket.send(data.encode())
                        for i in range(0, len(outputdata)):
                            self.client_socket.send(outputdata[i].encode())
                        self.client_socket.send("\r\n".encode())
                    
        
                else:
                    #print("else")    
                    data_rcv = server.recv(1024)
                    data_rcv=data_rcv.decode()
                    
                    print ('proxy-forward, client, '+str(self.thread_id)+" "+str(self.timestamp))
                    self.client_socket.send("HTTP/1.1 200 OK\r\n".encode())
                    self.client_socket.send("Content-Type: text/html\r\n".encode())
                    self.client_socket.send(data.encode())
                    for i in range(0, len(data_rcv)):
                        self.client_socket.sendall(data_rcv[i].encode())
                    self.client_socket.send("\r\n".encode())
                    cached_responses[filename] = [host_name,time_req]
                    if not os.path.exists(cache_dir):
                        os.makedirs(cache_dir)
                    with open(cache_dir + filename, 'w') as f:
                        f.write(data_rcv)
                server.close()
                self.client_socket.close()
                break
        finally:
            self.client_socket.close()
            
class ProxyServer(threading.Thread):
    def __init__(self, port):
        super(ProxyServer, self).__init__()
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('149.125.111.135', self.port))
        self.server_socket.listen(50)
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
            (client_socket, client_address) = self.server_socket.accept()
            thread_id = self.get_thread_id()
            timestamp = self.get_timestamp()
            handleClient = HandleClient(client_socket, ('149.125.38.91', 1234), self.port, thread_id, timestamp)
            handleClient.start()

if __name__ == '__main__':
    proxy_server = ProxyServer(8081)
    proxy_server.start()
    print("start")