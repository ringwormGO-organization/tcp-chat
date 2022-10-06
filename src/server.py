import socket
import threading

import colorama

host = None
port = None

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            client.remove()
            client.close()

            nickname = nicknames[index]
            broadcast(colorama.Fore.RED + f"{nickname} left the chat!".encode('ascii') + colorama.Fore.RESET)
            nicknames.remove(nickname)

            break

def receive():
    while True:
        client, address = server.accept()
        print(colorama.Fore.GREEN + f"Connected with {str(address)}" + colorama.Fore.RESET)

        client.send("NICK".encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is: {nickname}!\n")
        broadcast(f"{nickname} joined the chat!\n".encode('ascii'))
        client.send("Connected to the server!\n".encode('ascii'))

        thread = threading.Thread(target=handle, args=(client, ))
        thread.start()

if __name__ == "__main__":
    colorama.init()
    print(colorama.Fore.LIGHTRED_EX + "ringwormGO TCP CHAT version".center(100))
    print(colorama.Fore.LIGHTCYAN_EX + "((server, second generation))".center(100) + colorama.Fore.RESET)

    host = input("Enter an IP address: ")
    port = int(input("Enter a port: "))

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    print("Server is listening...\n")
    receive()
