import socket
import threading
import sys

sys.stdout.reconfigure(encoding='utf-8')

HOST = input("Enter server IP address: ")

while True:
    try:
        PORT = int(input("Enter server port: "))
        if 1024 <= PORT <= 65535:
            break
        else:
            print("Port must be between 1024 and 65535.")
    except ValueError:
        print("Invalid port. Enter a number.")


def receive_messages(sock):
    try:
        while True:
            data = sock.recv(4096)
            if not data:
                print("\n[DISCONNECTED FROM SERVER]")
                break
            print(data.decode("utf-8"), end="")
    except:
        print("\n[CONNECTION LOST]")
    finally:
        sock.close()

def send_input(sock):
    try:
        while True:
            message = input()
            sock.sendall(message.encode("utf-8"))
    except:
        sock.close()

def start_client():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        print(f"[CONNECTED TO SERVER {HOST}:{PORT}]")

        # Thread to receive messages
        threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

        # Main thread sends user input
        send_input(client)

    except ConnectionRefusedError:
        print("[ERROR] Could not connect. Is the server running?")
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    start_client()