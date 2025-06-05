import socket
import os

def save_received_file(conn, filename):
    try:
        received_data = b''
        while True:
            chunk = conn.recv(1024)
            if not chunk:
                print("Connection closed unexpectedly.")
                return None

            if b'EOF' in chunk:
                received_data += chunk.split(b'EOF')[0]
                break

            received_data += chunk

        new_filename = f"downloaded_{filename}"
        with open(new_filename, 'wb') as f:
            f.write(received_data)

        print(f"File saved as: {new_filename}")
        print(f"Total bytes received: {len(received_data)}")
        return len(received_data)

    except Exception as e:
        print(f"Error during file reception: {e}")
        return None

client = socket.socket()
ip_port = input("Enter server IP and port: ")
ip, port = ip_port.split(':')   
port = int(port)
try:
    client.connect((ip, port))
except Exception as e:
    print(f"Failed to connect to server: {e}")
    exit()
welcome_msg = client.recv(1024).decode('utf-8', errors='ignore')
print(f"Server message: {welcome_msg}")

while True:
    user_input = input("Enter command (GET <filename> or 'exit' to quit): ")

    if not user_input.strip():
        print("Empty command, please try again.")
        continue
    elif user_input.lower() == 'exit':
        print("Closing connection.")
        client.sendall(b'exit')
        break
    elif user_input.startswith('GET '):
        client.sendall(user_input.encode('utf-8'))

        response = client.recv(1024).decode('utf-8', errors='ignore')
        
        if response.startswith('Error: File'):
            print(response)
            continue
        elif response == 'READY_TO_SEND':
            client.sendall(b'READY')
            print("Ready to receive file...")
        
        filename = user_input[4:].strip()
        result = save_received_file(client, filename)

        if result is None:
            print("File transfer failed.")
        else:
            print("File transfer completed successfully.")
    elif user_input.lower() == 'close':
        close_input = input("You want to close the remote server[yes/no]")
        if close_input.lower() == 'yes' or close_input.lower() == 'y':
            print("Server is shutting down.")
            client.sendall(b'close')
            break
        else:
            continue
    else:
        print("Unknown command. Please use 'GET <filename>' or 'exit'.")
client.close()
print("Connection closed.")