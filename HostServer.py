# ================================================
# Console chat server by syika
# ================================================

import socket
import msvcrt

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind(('0.0.0.0', 8888))
server.listen(1)
print("[+] Waiting for client connection...")

client_socket, client_address = server.accept()
print(f"[+] Client connected from {client_address}")

client_socket.setblocking(False)
current_input = ""
print("[Server]: ", end="", flush=True)

while True:
    try:
        data = client_socket.recv(4096).decode('utf-8')
        if not data or data.lower() == 'exit':
            print("\n[+] Client disconnected")
            break
        print(f"\r[client]: {data}\n[Server]: {current_input}", end="", flush=True)
    except BlockingIOError:
        pass

    if msvcrt.kbhit():
        char = msvcrt.getch()
        
        if char == b'\r':
            print()
            if current_input.lower() == 'exit':
                break
            client_socket.send(current_input.encode('utf-8'))
            current_input = ""
            print("[Server]: ", end="", flush=True)
            
        elif char == b'\x08':
            if len(current_input) > 0:
                current_input = current_input[:-1]
                print('\b \b', end="", flush=True)
                
        else:
            try:
                decoded_char = char.decode('utf-8')
                current_input += decoded_char
                print(decoded_char, end="", flush=True)
            except UnicodeDecodeError:
                pass

client_socket.close()
server.close()