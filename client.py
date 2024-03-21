import socket
import sys
import os

#ip = input('Введите IP адрес сервера: ')
ip = "127.0.0.1"
#port = int(input('Введите порт сервера: '))
port = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip, port))

nickname = input('Введите ваш nickname: ')
client.send(nickname.encode())
os.system('cls' if os.name == 'nt' else 'clear')
data = client.recv(1024).decode()
print(data)

while True:
    message = input('Введите сообщение: ')
    os.system('cls' if os.name == 'nt' else 'clear')
    if message.lower() == 'exit':
        break
    client.send(message.encode())
    data = client.recv(1024).decode()
    print(data)

print("Соеденение с сервером завершенно")
client.close()