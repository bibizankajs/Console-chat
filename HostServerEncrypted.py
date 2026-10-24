# ================================================
# Encrypted Console chat server by syika
# ================================================

import socket
import msvcrt
from cryptography.fernet import Fernet

SHARED_KEY = b'4Vz7qX9Y_8W0pL2kM3nJ5bR8vC1xZ0aQ9wE8rT7yU6o=' 
cipher = Fernet(SHARED_KEY)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind(('0.0.0.0', 8888))
server.listen(1)
print("[+] Waiting for client connection (Encrypted Mode)...")

client_socket, client_address = server.accept()
print(f"[+] Client connected from {client_address}")

client_socket.setblocking(False)
current_input = ""
rx_buffer = b""
expected_length = None

print("[Server]: ", end="", flush=True)

while True:
    try:
        chunk = client_socket.recv(4096)
        if not chunk:
            print("\n[+] Client disconnected")
            break
        rx_buffer += chunk
    except BlockingIOError:
        pass

    if expected_length is None and len(rx_buffer) >= 4:
        expected_length = int.from_bytes(rx_buffer[:4], 'big')
        rx_buffer = rx_buffer[4:]

    if expected_length is not None and len(rx_buffer) >= expected_length:
        encrypted_data = rx_buffer[:expected_length]
        rx_buffer = rx_buffer[expected_length:]
        expected_length = None  

        try:
            decrypted_message = cipher.decrypt(encrypted_data).decode('utf-8')
            if decrypted_message.lower() == 'exit':
                print("\n[+] Client disconnected.")
                break
            print(f"\r[client]: {decrypted_message}\n[Server]: {current_input}", end="", flush=True)
        except Exception:
            print(f"\r[!] Warning: Decryption failed\n[Server]: {current_input}", end="", flush=True)

    if msvcrt.kbhit():
        char = msvcrt.getch()
        
        if char == b'\r':
            print()
            if current_input.lower() == 'exit':
                break
            
            encrypted_msg = cipher.encrypt(current_input.encode('utf-8'))
            msg_length = len(encrypted_msg).to_bytes(4, 'big')
            client_socket.sendall(msg_length + encrypted_msg)
            
            current_input = ""
            print("[Server]: ", end="", flush=True)
            
        elif char == b'\x08':
            if len(current_input) > 0:
                current_input = current_input[:-1]
                print('\b \b', end="", flush=True)
                
        else:
            try:
                decoded_char = char.decode('utf-8', errors='ignore')
                current_input += decoded_char
                print(decoded_char, end="", flush=True)
            except Exception:
                pass

client_socket.close()
server.close()