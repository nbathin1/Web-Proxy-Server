import socket
import threading
import datetime
#used to forward data from client to server
class HandleClient(threading.Thread):
    def __init__(self, client_socket, server_address, proxy_port, thread_id, timestamp):
        super(HandleClient, self).__init__()
        self.client_socket = client_socket
        self.server_address = server_address
        self.proxy_port = proxy_port
        self.thread_id = thread_id
        self.timestamp = timestamp

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect(self.server_address)
        while True:
            data = self.client_socket.recv(1024)
            #print(data)
            if data:
                print ('proxy-forward, server, '+str(self.thread_id)+" "+str(self.timestamp))
                server_socket.sendall(data)
            else:
                break
            data_rcv = server_socket.recv(1024)
            data_rcv=data_rcv.decode()
            #print(data_rcv)
            print ('proxy-forward, client, '+str(self.thread_id)+" "+str(self.timestamp))
            self.client_socket.send("HTTP/1.1 200 OK\r\n".encode())
            self.client_socket.send("Content-Type: text/html\r\n".encode())
            self.client_socket.send(data)
            for i in range(0, len(data_rcv)):
                self.client_socket.sendall(data_rcv[i].encode())
            self.client_socket.send("\r\n".encode())
            #print(data_rcv)
            self.client_socket.close()
            server_socket.close()
#proxy server 
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