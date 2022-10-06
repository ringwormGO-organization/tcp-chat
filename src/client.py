import socket
import threading

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
    host = input("Enter an IP address: ")
    port = int(input("Enter a port: "))
    nickname = input("Enter a nickname: ")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()
