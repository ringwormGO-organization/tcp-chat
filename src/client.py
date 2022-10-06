import socket
import threading

import colorama

nickname = None
client = None

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')

            if (message == "NICK"):
                client.send(nickname.encode('ascii'))

            else:
                print(message)

        except:
            print(message)
            client.close()
            break

def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))

if __name__ == "__main__":
    colorama.init()
    print(colorama.Fore.LIGHTRED_EX + "ringwormGO TCP CHAT version".center(100))
    print(colorama.Fore.LIGHTCYAN_EX + "((client, second generation))".center(100) + colorama.Fore.RESET)

    host = input("Enter an IP address: ")
    port = int(input("Enter a port: "))
    nickname = input("Enter a nickname: ")
    print(" ")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()
