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
            msg = message = client.recv(1024)

            if msg.decode('ascii').startswith("KICK"):
                if nicknames[clients.index(client)] == 'admin': # todo: roles
                    name_to_kick = msg.decode('ascii')[5:]
                    kick_user(name_to_kick)

                else:
                    client.send("Command was refused!\n")

            elif msg.decode('ascii').startswith("BAN"):
                if nicknames[clients.index(client)] == 'admin': # todo: roles
                    name_to_ban = msg.decode('ascii')[5:]
                    kick_user(name_to_ban)

                    with open("bans.txt", "a") as f: #todo: hash and/or databases
                        f.write(f"{name_to_ban}\n")

                    print(f"{name_to_ban} was banned!\n")

                else:
                    client.send("Command was refused!\n")

            else:
                broadcast(message)
        except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
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

        with open("bans.txt", "r") as f: # todo: load from hash and/or database
            bans = f.readlines()

        if nickname+'\n' in bans:
            client.send("BAN".encode('ascii'))
            client.close()
            continue

        if nickname == "admin": # todo: roles
            client.send("PASS".encode('ascii'))
            password = client.recv(1024).decode('ascii')

            if password != "adminpass": # todo: load from hash and/or databse
                client.send("REFUSE".encode('ascii'))
                client.close()
                continue

        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is: {nickname}!\n")
        broadcast(f"{nickname} joined the chat!\n".encode('ascii'))
        client.send("Connected to the server!\n".encode('ascii'))

        thread = threading.Thread(target=handle, args=(client, ))
        thread.start()

def kick_user(name):
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_kick = clients[name_index]

        clients.remove(client_to_kick)
        client_to_kick.send("You were kicked by an admin!\n".encode('ascii'))
        client_to_kick.close()

        nicknames.remove(name)
        broadcast(f"{name} was kicked!\n".encode('ascii'))

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
