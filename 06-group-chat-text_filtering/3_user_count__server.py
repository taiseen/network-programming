import threading
import socket
import matplotlib.pyplot as plt   # pip install matplotlib
import numpy as np


# localhost
host = "127.0.0.1"
# do not take any reserved or well known ports
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []


# total user count that present at system...
def total_user_count(userName):
    
    # display info at CLI
    if userName:
        print('------------------------------------')
        print('Total user present :', len(nicknames))
        print('Users name are :', nicknames)
        print('------------------------------------')

    # store in extra document
    if len(nicknames) != 0:
        with open('user_list.txt', 'w') as file_handle:
            for f in nicknames:
                file_handle.write(f'{f}\n')


# broadcasting messages from the server to all the clients
def broadcast(message):
    # implement the filtering of the messages here
    # implement the brand analytics and tracking here

    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            # receiving 1024 bytes
            message = client.recv(1024)
            broadcast(message)

        except:
            # find out the index of the failed client frm the clients list
            index = clients.index(client)
            clients.remove(client)
            client.close()

            # we also remove the nickname of the removed client
            nickname = nicknames[index]
            broadcast(f"@ @ @ @ @ @ {nickname} left the chat!".encode('ascii'))
            nicknames.remove(nickname)

            break


def receive():
    while True:
        print("receive function is running on the server!")
        # returns a tuple
        client, address = server.accept()

        # you have cut down the address str type casting
        print(f"Connected with {str(address)}")

        # we need to ask the client for the nickname
        # made change here
        name = "NICK"
        client.send(name.encode('ascii'))

        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # user present count system...
        total_user_count(name)

        # print only at server side cli...
        print(f"Nickname of the client is =====> {nickname}")

        # server send info to all users...
        broadcast(f"=====> {nickname} joined the chat".encode('ascii'))

        # letting know the specific client that it has connected to the server
        client.send("Connected to the server".encode('ascii'))

        # define and run a thread
        # because we want to be able to handle multi clients same time

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


# main method
print("Server is running ✅✅✅")
receive()
