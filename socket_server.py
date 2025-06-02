import socket
import os

socket_server = socket.socket()
socket_server.bind(('localhost', 8888))

socket_server.listen(1)
print("Server is listening on port 8888...")

while True:
    conn, address = socket_server.accept()
    print(f"Connection from {address} has been established.")
    msg = "Successfully connected to the server!"
    conn.sendall(msg.encode('utf-8'))

    try:
        while True:     
            command = conn.recv(1024).decode('utf-8')

            if not command:
                print("No command received, closing connection.")
                break

            print(f"Received command: {command}")
            if command.lower() == 'exit':
                print("Exit command received, closing connection.")
                conn.sendall(b"Connection closed.")
                break
            
            elif command.startswith('GET '):
                filename = command[4:].strip()
                file_path = os.path.join(os.getcwd(), filename)

                if not os.path.isfile(file_path):
                    error_msg = f"Error: File '{filename}' does not exist."
                    conn.sendall(error_msg.encode('utf-8'))
                    print(error_msg)
                    continue
                else:
                    
                    # file_size = os.path.getsize(file_path)
                    # conn.sendall(str(file_size).ljust(16).encode('utf-8'))

                    
                    total_bytes_sent = 0
                    with open(file_path, 'rb') as file:
                        while True:
                            data = file.read(1024)
                            if not data:
                                break
                            conn.sendall(data)
                            total_bytes_sent += len(data)
                    print(f"Sent {total_bytes_sent} bytes of file '{filename}' to {address}.")
                    conn.sendall(b'EOF')
            else:
                conn.sendall('Unknown command. Please use "GET <filename>" or "exit".'.encode('utf-8'))
    except Exception as e:  
        print(f"An error occurred: {e}")
    finally:
        conn.close()
        print(f"Connection with {address} closed.")
    conn.close()