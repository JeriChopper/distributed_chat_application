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
import threading

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5555
BUFFER_SIZE = 1024


### Function to receive messages
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(BUFFER_SIZE).decode()
            print(message)
        except Exception as e:
            print(e)
            break

### Function to send messages
def send_message(client_socket):
    while True:
        message = input()
        if message == '/quit':
            client_socket.close()
            break
        client_socket.send(message.encode())


### Main function which asks for authentication and handles interaction
### Based on server response which comes from the socket, it will handle authentication accordingly

if __name__ == "__main__":
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print("Connected to the server")

        username = input("Enter your username: ")
        password = input("Enter your password: ")

        client_socket.send(f"{username},{password}".encode())

        response = client_socket.recv(BUFFER_SIZE).decode()

        if response == "LOGIN":
            print("You are logged in.")
        elif response == "REGISTER":
            print("You don't have an account. Please register.")
            while True:
                try:
                    new_username = input("Enter your new username: ")
                    new_password = input("Enter your new password: ")
                    email = input("Enter your email: ")
                    client_socket.send(f"{new_username},{new_password},{email}".encode())
                    register_response = client_socket.recv(BUFFER_SIZE).decode()

                    if register_response == "REGISTER_SUCCESS":
                        print("Registration successful. You are now logged in.")
                        break
                    elif register_response == "USERNAME_TAKEN":
                        print("Username already taken. Please choose a different username.")

                except Exception as e:
                    print("An error occurred during registration:", e)
                    break

        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        send_thread = threading.Thread(target=send_message, args=(client_socket,))
        receive_thread.start()
        send_thread.start()

        receive_thread.join()
        send_thread.join()

        client_socket.close()
    except Exception as e:
        print("Unexpected error occurred:", e)
