"""
Distributed Systems Project
24.04.2024

Sources used for creation of code:

Distributed Systems Assignment 4 was used as inspiration

https://www.youtube.com/watch?v=3UOyky9sEQY This video helped in learning the basics
https://docs.python.org/3.9/library/socket.html Helped to understand python socket protocols as a whole
https://docs.python.org/3.9/library/threading.html Helped to understand python threading protocols
https://realpython.com/python-sockets/#socket-api-overview Helped to understand socket communication
"""

import socket
import sqlite3
import threading

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5555
BUFFER_SIZE = 1024

# Dictionary to store clients
clients = {}


### Authenticate user function checks if a user has registered and can be found in db. Used for logging in.
def authenticate_user(username, password):
    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM users
                      WHERE username = ? AND password = ?''', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None


### Register user function inserts register values in to db
def register_user(username, password, email):
    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''INSERT INTO users (username, password, email)
                          VALUES (?, ?, ?)''', (username, password, email))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


### Messages sent are implemented in db (To retrieve them etc)
def insert_message(sender, message, recipient=None, private=False):
    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO messages (sender, recipient, message, private)
                      VALUES (?, ?, ?, ?)''', (sender, recipient, message, private)) ### avoids sql injections with proper use of cursor
    conn.commit()
    conn.close()

### Handles clients within the server
def handle_client(client_socket, client_address):
    data = client_socket.recv(BUFFER_SIZE).decode()
    username, password = data.split(',')
    
    ### Use socket messages to do interactive authenticaton / registration
    if authenticate_user(username, password):
        clients[client_socket] = username
        client_socket.send("LOGIN".encode())
        broadcast(f"{username} has joined the chat.")
    else:
        client_socket.send("REGISTER".encode())
        data = client_socket.recv(BUFFER_SIZE).decode()
        new_username, new_password, email = data.split(',')
        if register_user(new_username, new_password, email):
            client_socket.send("REGISTER_SUCCESS".encode())
            clients[client_socket] = new_username
            broadcast(f"{new_username} has joined the chat.")
        else:
            client_socket.send("USERNAME_TAKEN".encode())
            client_socket.close()
            return


    while True:
        try:
            message = client_socket.recv(BUFFER_SIZE).decode()
            if not message:
                break
            if message.startswith('@'):
                recipient, message = message.split(maxsplit=1)
                recipient = recipient[1:]
                for client_sock, nick in clients.items():
                    if nick == recipient:
                        client_sock.send(f'(Private) {clients[client_socket]}: {message}'.encode())
                        insert_message(clients[client_socket], message, recipient=recipient, private=True) ### private messages added to DB with different parameters
                        break
            else:
                sender = clients[client_socket]
                insert_message(sender, message)
                broadcast(f"{sender}: {message}")
        except Exception as e:
            print(e)
            break
    
    ### Delete clients if they leave and inform with message        
    if client_socket in clients:
        username = clients[client_socket]
        del clients[client_socket]
        broadcast(f"{username} has left the chat.")

    client_socket.close()


### Broadcast messages
def broadcast(message):
    for client_sock in clients:
        client_sock.send(message.encode())

### Start server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen()

    print(f'Server is listening on {SERVER_HOST}:{SERVER_PORT}')

    while True:
        client_socket, client_address = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

### Main function
if __name__ == "__main__":
    start_server()