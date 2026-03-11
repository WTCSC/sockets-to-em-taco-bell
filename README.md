# Pokémon Battle Server – Documentation

This documentation explains how the Pokémon server works, how battles function, and how to connect using `client.py`. It covers setup, running the server, running the client, and internal logic of battle mechanics and sockets.

---

## Overview

This project is a multiplayer Pokémon battle system using Python sockets. Players connect using `client.py`, choose a Pokémon, and battle another connected player.

- `server.py` – Handles connections, manages players, runs battles.
- `client.py` – Connects to the server, displays messages, sends input.

---

## Requirements

No external libraries are needed. Only built-in Python modules:

socket
threading
random

Python 3.8+ recommended.

---

## How to Run the Server

Run:

python server.py


- **HOST:** 0.0.0.0  
- **PORT:** 5555

The server now waits for players to connect using `client.py`.

---

## How to Run the Client

Each player runs:

python client.py


Example `client.py` snippet:

```python
import socket

HOST = "127.0.0.1"  # or server IP
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

while True:
    server_msg = client.recv(4096).decode()
    print(server_msg)
    if "(input)" in server_msg:
        client.send(input("> ").encode())

```

## How it works:

Client connects to server

Receives messages (battle events, HP updates, menus)

Sends input when prompted

Players do not connect directly to each other

## How Battles Work

The server uses this Pokémon data structure:

{
    "Charizard": { "hp": 120, "attack": 30, "art": "ASCII..." },
    "Gengar":    { "hp": 100, "attack": 35, "art": "ASCII..." },
    "Mewtwo":    { "hp": 130, "attack": 25, "art": "ASCII..." }
}

Server Architecture
Threading Model

Each client runs in its own thread. When two players are paired, a battle thread starts.

accept_connections() – waits for clients

client_thread() – handles individual player

battle_thread() – manages the battle loop

## Example Gameplay 

Connected to Pokémon Battle Server!
Choose your Pokémon:
1) Charizard
2) Gengar
3) Mewtwo
(input)

Waiting for another player...

Battle Start!
You chose Charizard!
Opponent chose Gengar!

Your turn! (input)
> attack

You dealt 30 damage!
Opponent HP: 70

Opponent attacked you!
You took 35 damage!
Your HP: 85

## Networking Diagram

Player A (client.py)
       |
       |----> server.py ----> Battle Logic
       |
Player B (client.py)

## Troubleshooting

"Connection refused"

Server not running

Wrong IP in client.py

Firewall blocking port 5555

ASCII art broken?

Your terminal may not support Unicode.

Battle not starting?

You must have two connected clients.


---

This is **ready to paste** into your GitHub `README.md`.  

If you want, I can also **add some extra styling tricks** like headers, emojis, and nicer-looking code blocks that still work in Markdown, to make it closer to your HTML style.  

Do you want me to do that next?
