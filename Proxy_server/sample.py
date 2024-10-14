import socket
import sys
import threading
import time

def start():  # Main Program
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', 8080))
        sock.listen(10)
        print("[*] Server started successfully [ %d ]" % (10))

        while True:
            conn, addr = sock.accept()  # Accept connection from client browser
            data = conn.recv(1024)  # Recieve client data
            threading.Thread(target=proxy_server, args=("localhost",1234,conn,addr,data)).start()


def proxy_server(webserver, port, conn, addr, data):
    try:
        print("Success")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((webserver, port))
        sock.send(data)
        starttime = time.time()
        print("proxy-foward" +  " ," + webserver.decode()  + " ,"  + threading.current_thread().name + " ,"  + time.ctime(starttime))
        while 1:
            reply = sock.recv(1024)
            transfertime=time.time()
            if (len(reply) > 0):
                conn.send(reply)
                webserveraddr=addr[0]
                print("proxy-foward" + " ," + webserveraddr +  " ,"  + threading.current_thread().name +  " ,"  +time.ctime(transfertime))

            else:
                break

        sock.close()

        conn.close()
    except socket.error:
        sock.close()
        conn.close()
        print(sock.error)
        sys.exit(1)


if __name__ == "_main_":
    start()