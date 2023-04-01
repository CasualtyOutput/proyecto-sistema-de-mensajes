import socket
import sys

name = input("Write your name: ")

if(len(sys.argv) > 1): 
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((sys.argv[1], 8080))
    msg = clientsocket.recv(1024).decode("utf-8")
    print(name + ": " + str(msg))

    while True:
        msg = input(name + ": ")
        clientsocket.send(bytes(name + ": " +msg, "utf-8"))

        msg = clientsocket.recv(1024).decode("utf-8")

        print(name + ": " + str(msg))

        if msg.lower() == "!exit":
            break
else:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hostName = socket.gethostname()
    s.bind((hostName, 8080))
    s.listen(1)

    print("Waiting for any incoming connections ...")
    clientsocket, address = s.accept()

    print(f"Connection from {address} has been established!")
    clientsocket.send(bytes(f"Welcome to {name}'s chat room!", "utf-8"))

    while True:
        msg = clientsocket.recv(1024).decode("utf-8")
        if not msg:
            break
        print(str(msg))
        msg = input(name + ": ")
        clientsocket.send(bytes(msg, "utf-8"))

clientsocket.close()