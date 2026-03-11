import socket
import random

HOST = input("Enter server IP (localhost if same machine): ")
PORT = int(input("Enter server port: "))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# Receive initial messages
while True:
    data = s.recv(1024).decode()
    if not data:
        break
    print(data, end='')
    if "Choose your Pokémon" in data:
        break

# Choose Pokémon
while True:
    choice = input("Your Pokémon: ")
    s.send(choice.encode())
    break

# Battle loop
while True:
    data = s.recv(1024).decode()
    if not data:
        break

    if "YOUR TURN" in data:
        # It's client's turn
        print("\nYour turn!")
        action = input("Choose action (attack/heal): ").strip().lower()
        if action == "attack":
            dmg = random.randint(20, 35)  # random attack damage for client
            s.send(f"attack {dmg}".encode())
        elif action == "heal":
            heal_amount = random.randint(20, 35)
            s.send(f"heal {heal_amount}".encode())
        else:
            s.send("skip".encode())
    else:
        print(data)

    if "fainted" in data:
        break

s.close()