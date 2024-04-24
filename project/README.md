# Distributed Chat Application

This is a distributed chat application implemented in Python using sockets and SQLite. It allows users to register, login, send messages to each other, including private messages, and stores messages in a SQLite database.

## Features

- **User Authentication**: Users can register/login
- **Real-time Messaging**: Users can chat real-time
- **Private Messaging**: Users can send private messages
- **Message Storage**: All messages are stored in a SQLite database
- **Multithreaded Server**: The server can handle multiple client connections

## Installation

1) Clone repository: git clone https://github.com/JeriChopper/dist_system_chat
2) Navigate to the project directory
3) Install latest version of sqlite3 and python3 with command: pip install sqlite3


## HOW-TO

1) Open command prompts or terminals
2) Navigate to application folders
3) Run command: python3 db_script.py to make sure chat.db is created with proper functionality
4) Run command: python3 server.py on another terminal
5) Run command: python3 client.py on another terminal

