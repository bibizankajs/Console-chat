# ================================================
# Encrypted Console chat client by syika
# ================================================

import msvcrt
import socket
from cryptography.fernet import Fernet

SHARED_KEY = b'4Vz7qX9Y_8W0pL2kM3nJ5bR8vC1xZ0aQ9wE8rT7yU6o='
cipher = Fernet(SHARED_KEY)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8888))
print("[+] You Connected to the server (Encrypted Mode)")

client.setblocking(False)
current_input = ""
rx_buffer = b""
expected_length = None

print("[Client]: ", end="", flush=True)

while True:
    try:
        chunk = client.recv(4096)
        if not chunk:
            print("\n[!] Server closed connection.")
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
                print("\n[!] Server closed connection.")
                break
            print(f"\r[server]: {decrypted_message}\n[Client]: {current_input}", end="", flush=True)
        except Exception:
            print(f"\r[!] Warning: Decryption failed\n[Client]: {current_input}", end="", flush=True)

    if msvcrt.kbhit():
        char = msvcrt.getch()
        
        if char == b'\r':
            print()
            if current_input.lower() == 'exit':
                break
            
            encrypted_msg = cipher.encrypt(current_input.encode('utf-8'))
            msg_length = len(encrypted_msg).to_bytes(4, 'big')
            client.sendall(msg_length + encrypted_msg)
            
            current_input = ""
            print("[Client]: ", end="", flush=True)
            
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

client.close()