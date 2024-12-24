import os
import socket
import threading
os.system ("clear")
print(''' 
{version: BETA}
{Creator: Debajit.KTY} ''')
input("Press enter to start...")
os.system ("clear")
clients = []  # List to keep track of connected clients

def handle_client(conn, addr):
    print(f"Connected to Device 2.")
    clients.append(conn)  # Add the new client to the list
    try:
        while True:
            message = conn.recv(1024).decode()
            if not message:
                break
            print(f'''
From Device 2: {message} ''')
            broadcast(f'''
From Device 2: {message} ''', conn)  # Broadcast the message to all clients
    finally:
        conn.close()
        clients.remove(conn)  # Remove the client from the list
        print(f'''
Connection from Device 2 has been closed. ''')

def broadcast(message, sender_conn):
    for client in clients:
        if client != sender_conn:  # Don't send the message back to the sender
            try:
                client.sendall(message.encode())
            except Exception as e:
                print(f"Error sending message to a client: {e}")

def start_server():
    host = '0.0.0.0'  # Listen on all interfaces
    port = 12345       # Port to listen on

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server is running on {host}:{port}")

    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

def server_send_messages():
    while True:
        message = input("Device 1: ")
        if message.lower() == 'exit':
            break
        broadcast(f"Device 1: {message}", None)  # Broadcast to all clients

if __name__ == "__main__":
    threading.Thread(target=server_send_messages, daemon=True).start()  # Start the message sending thread
    start_server()
