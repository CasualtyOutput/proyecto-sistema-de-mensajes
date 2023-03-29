import socket

def connect(hostname, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)
    result = sock.connect_ex((hostname, port))
    sock.close()
    return result == 0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
hasHost = True
port = 8080

try:
    s.connect((host, port))
except:
    hasHost = False

if(hasHost):
    name = input("Write your name: ")
    while True:
        msg = s.recv(1024)
        print(msg.decode("utf-8"))

else:
    print("No open chat room found. Creating a new one.")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host,port))
    s.listen(5)
    name = input("Write your name: ")
    
    for i in range(0,255):
        res = connect("192.168.1."+str(i), 22)
        if res:
            print("Device found at: ", "192.168.1."+str(i) + ":"+str(22))
    
    print("Waiting for any incoming connections ...")
    while True:
        clientsocket,address = s.accept()
        print(f"Connection from {address} has been established!")
        clientsocket.send(bytes(f"Welcome to {name}'s chat room!", "utf-8"))