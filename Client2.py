# ==============================
# client for server by syikaa
# ==============================

import msvcrt
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(('127.0.0.1', 8888))
print("[+] You Connected to the server")

client.setblocking(False)
current_input = ""
print("[Client]: ", end="", flush=True)

while True:
    try:
        data = client.recv(4096).decode('utf-8')
        if not data or data.lower() == 'exit':
            print("\n[!] Server closed connection.")
            break 
        print(f"\r[server]: {data}\n[Client]: {current_input}", end="", flush=True)
    except BlockingIOError:
        pass

    if msvcrt.kbhit():
        char = msvcrt.getch()
        
        if char == b'\r':
            print()
            if current_input.lower() == 'exit':
                break
            client.send(current_input.encode('utf-8'))
            current_input = ""
            print("[Client]: ", end="", flush=True)
            
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

client.close()