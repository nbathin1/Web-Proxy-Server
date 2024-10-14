import socket
import threading
import datetime

HOST = 'localhost'
PORT = 1234
i=1

# create a socket and bind to the host and port
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))


server.listen(10)


def handleClient(clientSocket,i):
    try:
        print("server-response, "+str(i)+" "+str(datetime.datetime.now()))
        data = client.recv(1024).decode()
        filename = data.split()[1]
        f = open(filename[1:])
        outputdata=f.read()
        client.sendall(outputdata.encode())
        client.close()
        f.close()
        clientSocket.close()
    except IOError:
        client.send("<html><head></head><body><h1><b>404 File Not Found<b></h1></body></html>\r\n".encode())
    
    
while True:
    # accept new connection
    client, addr = server.accept()
    clientHandler = threading.Thread(target=handleClient, args=(client,i))
    clientHandler.start()
    i=i+1
    