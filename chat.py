import socket
import sys

name = input("Write your name: ")

def encode(msg) : 
    msg_to_ascii = [ord(char) for char in msg]
    ascii_to_bytes = bytes(msg_to_ascii)

    return ascii_to_bytes

def decode(ascii_to_bytes) :
    bytes_to_ascii = [byte for byte in ascii_to_bytes]
    msg = ''.join([chr(code) for code in bytes_to_ascii])

    return msg

if(len(sys.argv) > 1): 
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((sys.argv[1], 8080))
    msg = decode(clientsocket.recv(1024))
    print(name + ": " + str(msg))

    while True:
        msg = input(name + ": ")
        clientsocket.send(bytes(name + ": " +msg, "utf-8"))

        msg = decode(clientsocket.recv(1024))

        print(str(msg))

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
    clientsocket.send(encode(f"Welcome to {name}'s chat room!"))

    while True:
        msg = clientsocket.recv(1024).decode("utf-8")
        if not msg:
            break
        print(str(msg))
        msg = input(name + ": ")
        clientsocket.send(encode(name + ": " + msg))

clientsocket.close()