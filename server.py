import socket
import random
import threading

HOST = "0.0.0.0"

# Choose port
while True:
    try:
        PORT = int(input("Enter port to host on (e.g. 5555): "))
        if 1024 <= PORT <= 65535:
            break
        else:
            print("Port must be between 1024 and 65535.")
    except ValueError:
        print("Invalid port. Enter a number.")

# Pokémon data
pokemon_data = {
    "Charizard": {"hp": 120, "attack": 30},
    "Gengar": {"hp": 100, "attack": 35},
    "Mewtwo": {"hp": 130, "attack": 25},
    "Blastoise": {"hp": 140, "attack": 28},
    "Lugia": {"hp": 115, "attack": 32},
    "Umbreon": {"hp": 125, "attack": 29},
}

# Server chooses its Pokémon
print("Choose your server Pokémon:")
for name in pokemon_data:
    print("-", name)

while True:
    server_pokemon_name = input()
    if server_pokemon_name in pokemon_data:
        server_pokemon = pokemon_data[server_pokemon_name].copy()
        break
    else:
        print("Invalid Pokémon. Pick again.")

# Set up server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
print(f"[SERVER] Listening on {HOST}:{PORT}...")

conn, addr = s.accept()
print(f"[CONNECTED] Client {addr} connected.")

# Ask client to pick Pokémon
conn.send("Welcome to Pokémon Battle!\nChoose your Pokémon:\n".encode())
for name in pokemon_data:
    conn.send(f"- {name}\n".encode())

client_choice = conn.recv(1024).decode().strip()
if client_choice not in pokemon_data:
    conn.send("Invalid Pokémon. Disconnecting.".encode())
    conn.close()
    exit()

client_pokemon = pokemon_data[client_choice].copy()
conn.send(f"You chose {client_choice}!\nBattle starts!\n".encode())

# Battle loop
turn = "server"  # server attacks first
while server_pokemon["hp"] > 0 and client_pokemon["hp"] > 0:
    if turn == "server":
        dmg = server_pokemon["attack"] + random.randint(-5, 5)
        client_pokemon["hp"] -= dmg
        msg = f"{server_pokemon_name} attacks {client_choice} for {dmg} damage! {client_choice} HP: {client_pokemon['hp']}\n"
        print(msg)
        conn.send(msg.encode())
        turn = "client"
    else:
        conn.send("YOUR TURN\n".encode())
        dmg = int(conn.recv(1024).decode())
        server_pokemon["hp"] -= dmg
        msg = f"{client_choice} attacks {server_pokemon_name} for {dmg} damage! {server_pokemon_name} HP: {server_pokemon['hp']}\n"
        print(msg)
        conn.send(msg.encode())
        turn = "server"

# End of battle
if server_pokemon["hp"] <= 0:
    conn.send(f"{server_pokemon_name} fainted! You win!\n".encode())
    print(f"{server_pokemon_name} fainted! Client wins!")
else:
    conn.send(f"{client_choice} fainted! Server wins!\n".encode())
    print(f"{client_choice} fainted! Server wins!")

conn.close()
s.close()