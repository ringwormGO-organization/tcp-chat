from math import nextafter
import socket
import threading

import colorama

nickname = None
password = None

client = None
stop_thread = False

def receive():
    while True:
        global stop_thread
        if stop_thread:
            break

        try:
            message = client.recv(1024).decode('ascii')

            if (message == "NICK"):
                client.send(nickname.encode('ascii'))
                next_message = client.recv(1024).decode('ascii')

                if next_message == "PASS":
                    client.send(password.encode('ascii'))

                    if client.recv(1024).decode('ascii'):
                        print("Connection was refused!\n")
                        stop_thread = True

                elif next_message == "BAN":
                    print("Connection refused because of ban!\n")
                    client.close()
                    stop_thread = True

            else:
                print(message)

        except:
            print(message)
            client.close()
            break

def write():
    while True:
        if stop_thread:
            break

        message = f'{nickname}: {input("")}'

        if message[len(nickname)+2:].startswith('/'):
            if nickname == 'admin': # todo: roles
                if message[len(nickname)+2:].startswith("/kick"):
                    client.send(f"KICK {message[len(nickname)+2+6:]}".encode('ascii'))

                elif message[len(nickname)+2:].startswith("/ban"):
                    client.send(f"BAN {message[len(nickname)+2+5:]}".encode('ascii'))

            else:
                print("Commands may be executed by admins only!\n")
                
        else:
            client.send(message.encode('ascii'))

if __name__ == "__main__":
    colorama.init()
    print(colorama.Fore.LIGHTRED_EX + "ringwormGO TCP CHAT version".center(100))
    print(colorama.Fore.LIGHTCYAN_EX + "((client, second generation))".center(100) + colorama.Fore.RESET)

    host = input("Enter an IP address: ")
    port = int(input("Enter a port: "))
    nickname = input("Enter a nickname: ")

    if nickname == "admin": # todo: roles
        password = input("Enter password: ")

    print(" ")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()
