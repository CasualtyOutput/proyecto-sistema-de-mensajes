import socket
import threading

clients = []
names = []
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
name = input("Write your name: ")

def encode(msg) : 
    msg_to_ascii = [ord(char) for char in msg]
    ascii_to_bytes = bytes(msg_to_ascii)

    return ascii_to_bytes

def decode(ascii_to_bytes) :
    bytes_to_ascii = [byte for byte in ascii_to_bytes]
    msg = ''.join([chr(code) for code in bytes_to_ascii])

    return msg
  
def broadcast(message):
    for client in clients:
        client.send(message)
    print(message.decode('utf-8'))
    
def manualBroadcast():
    while True:
        message = '{}: {}'.format(name, input(''))
        for client in clients:
            client.send(message.encode('utf-8'))

def handle(client):
    while True:
        try:
            message = client.recv(2048)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = names[index]
            broadcast(f'{nickname} left the chat!'.encode("utf-8"))
            names.remove(nickname)
            break
        
def receiveServer(server):
    while True:
        # Accept Connection
        client, address = server.accept()

        # Request And Store Nickname
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(2048).decode('utf-8')
        names.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        client.send("Welcome to {}'s server!".format(name).encode('utf-8'))
        broadcast("{} joined".format(nickname).encode('utf-8'))
        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
        
def receiveClient(client):
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(2048).decode('utf-8')
            if message == 'NICK':
                client.send(name.encode('utf-8'))
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break
        
def write(client):
    while True:
        message = '{}: {}'.format(name, input(''))
        client.send(message.encode('utf-8'))

validChoice = False
print("Do you want to [H]ost or [J]oin a chat room?")
while(not validChoice):
    hostOrClient = input().lower()
    if(hostOrClient == "j" or hostOrClient == "h"):
        validChoice = True
    else:
        print("Only input either <H> or <J>")
           

if(hostOrClient == "j"): 
    validChoice = False
    while(not validChoice):
        roomID = input("Insert chat room ID: ")
        
        hostName = socket.gethostname()
        hostIP = socket.gethostbyname(hostName)
        localIP = ".".join(hostIP.split(".")[:-1])
    
        if(s.connect_ex((localIP + "." + roomID, 8080)) == 0):
            validChoice = True
        else:
            print("Chat room not found")
    
    receive_thread = threading.Thread(target=receiveClient, args=(s,))
    receive_thread.start()
    
    write_thread = threading.Thread(target=write, args=(s,))
    write_thread.start()
    
        
elif(hostOrClient == "h"):
    print("Your room ID is:", socket.gethostbyname(socket.gethostname()).split(".").pop(-1))
    hostName = socket.gethostname()
    hostIP = socket.gethostbyname(hostName)
    s.bind((hostIP, 8080))
    s.listen()
    
    thread = threading.Thread(target=manualBroadcast)
    thread.start()
    receiveServer(s)