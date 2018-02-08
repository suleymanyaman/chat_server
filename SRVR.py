import socket
from threading import Thread

def accept_incoming_connections():
    while True:
        client, client_adress = SERVER.accept()
        client.send("Your messages are secured by encryption. Choose a nickname for yourself.".encode())
        print("%s:%s has connected" % client_adress)
        #adresses[client]=client_adress
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
    name = client.recv(1024).decode()
    welcome = 'Welcome %s! If you ever want to quit, type {EXIT} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "{} is online".format(name)
    broadcast(msg.encode())
    clients.append(client)


    while True:
        msg = client.recv(1024)
        if msg.decode() != "EXIT":
            broadcast(msg, name+": ")

        else:
            client.send("You're leaving...".encode())
            client.close()
            clients.remove(client)
            broadcast("{} is offline".format(name).encode())
            break

def broadcast(msg, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, "utf-8")+ msg)


clients=[]
adresses={}

HOST = "0.0.0.0"
PORT = 5000
ADDR = (HOST,PORT)

SERVER = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
SERVER.bind(ADDR)

if __name__== "__main__":
    SERVER.listen(5)
    print("Waiting for connection.....")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()




#listen, blocking-non blocking
