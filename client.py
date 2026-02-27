import socket
import random

host = input("Enter server IP address: ")
port = int(input("Enter server port: "))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

# Receive Pokémon options
data = s.recv(4096).decode()
print(data)

# Choose Pokémon
choice = input()
s.send(choice.encode())

while True:
    msg = s.recv(1024).decode()
    if "YOUR TURN" in msg:
        # Client attacks
        dmg = random.randint(20, 35)
        print(f"Attacking with {dmg} damage!")
        s.send(str(dmg).encode())
    else:
        print(msg)
        if "fainted" in msg:
            break

s.close()