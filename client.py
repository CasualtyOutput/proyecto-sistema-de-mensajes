import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostName = socket.gethostname()
hostIP = socket.gethostbyname(hostName)
localIP = ".".join(hostIP.split(".")[:-1])
roomID = hostIP.split(".").pop(-1)
port = 8080

print("Do you want to host or join a chat room?")
print("[1] Host a room")
print("[2] Join a room")
hostOrJoin = input()

if(hostOrJoin == "2"):
    roomID = input("Insert chat room ID: ")
    name = input("Write your name: ")
    s.connect((localIP + "." + roomID, 8080))
    while True:
        msg = s.recv(1024)
        print(msg.decode("utf-8"))

elif (hostOrJoin == "1"):
    print("Your room ID is:", roomID)
    s.bind((hostName,port))
    s.listen(5)
    name = input("Write your name: ")
    
    print("Waiting for any incoming connections ...")
    while True:
        clientsocket,address = s.accept()
        print(f"Connection from {address} has been established!")
        clientsocket.send(bytes(f"Welcome to {name}'s chat room!", "utf-8"))
