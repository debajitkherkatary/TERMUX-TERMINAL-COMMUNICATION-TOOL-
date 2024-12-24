import os
import socket
import threading
os.system ("clear")
print('''
{Version: BETA}
{Creator: Debajit.KTY} ''')
input("Press enter to start...")
os.system ("clear")
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(message)
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def send_message(client_socket):
    while True:
        message = input("You: ")
        if message.lower() == 'exit':
            break
        client_socket.sendall(message.encode())
    client_socket.close()

def start_client():
    host = input("Enter the Device 1 IP address: ")  # e.g., 192.168.1.100
    port = 12345  # Port to connect to

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()
    send_message(client_socket)

if __name__ == "__main__":
    start_client()