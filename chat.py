import socket
import threading
import logging

logging.basicConfig(level = logging.INFO, filename="log.log", filemode="w",
                    format="%(asctime)s - %(levelname)s - %(message)s")

clients = []
names = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

name = input("Write your name: ")
logging.info("User submited name <" + str(name) +">")

def encode(msg) : 
    msg_to_ascii = [ord(char) for char in msg]
    ascii_to_bytes = bytes(msg_to_ascii)
    logging.info("Message sent by <" + str(name) +">" + " was encoded")

    return ascii_to_bytes

def decode(ascii_to_bytes) :
    bytes_to_ascii = [byte for byte in ascii_to_bytes]
    msg = ''.join([chr(code) for code in bytes_to_ascii])
    logging.info("Message received by <" + str(name) +">" + " was decoded")

    return msg
  
def broadcast(message):
    for client in clients:
        client.send(message)
    print(message.decode('utf-8'))
    logging.info("Received message was sent to all connected clients")
    
def manualBroadcast():
    while True:
        message = '{}: {}'.format(name, input(''))
        for client in clients:
            client.send(message.encode('utf-8'))
    logging.info("Message received by <" + str(name) +">" + " (Host)" + " was shown")

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
            logging.info("<" + str(nickname) + ">" + " left the chatroom")
            break
        
def receiveServer(server):
    logging.info("Chat room created successfully")
    while True:
        client, address = server.accept()

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(2048).decode('utf-8')
        names.append(nickname)
        clients.append(client)

        client.send("Welcome to {}'s server!".format(name).encode('utf-8'))
        broadcast("{} joined".format(nickname).encode('utf-8'))
        
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
        logging.info("Started a new thread for user <" + str(nickname) + ">")
        
def receiveClient(client):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message == 'NICK':
                client.send(name.encode('utf-8'))
            else:
                print(message)
        except:
            print("An error occured!")
            client.close()
            logging.error("Client disconnected due to erro when receiving message")
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
    logging.info("User chose to join a chat room")
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
    
    logging.info("User successfully joined a chat room")
    
        
elif(hostOrClient == "h"):
    logging.info("User chose to host a chat room")
    print("Your room ID is:", socket.gethostbyname(socket.gethostname()).split(".").pop(-1))
    hostName = socket.gethostname()
    hostIP = socket.gethostbyname(hostName)
    s.bind((hostIP, 8080))
    s.listen()
    
    thread = threading.Thread(target=manualBroadcast)
    thread.start()
    receiveServer(s)