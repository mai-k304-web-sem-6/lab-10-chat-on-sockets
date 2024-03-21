import socket
import threading
import os
from datetime import datetime

# Переменные окружения
MAX_CLIENTS = 10 # Максимальное количество клиентов
clients = [] # Динамический массив для хранения информации о клиентах
server_host = "127.0.0.1" # Хост сервера
server_port = 12345 # Порт сервера

def handle_client(client_socket, client_address): # Функция для обработки клиентов
    # Предварительная подготовка для подключения клиента
    nickname = client_socket.recv(1024).decode() # Получение кодового имени клиента
    if not nickname: # Если имя клиента не введено
        return # Выход из программы
    clients.append({"socket": client_socket, "address": client_address, "nickname": nickname}) # Добавление нового клиента в список
    with open("server.log", "r") as file:
        lines = file.readlines()
        last_messages = lines[-20:] if len(lines) > 20 else lines
        for message in last_messages:
            client_socket.send(message.encode())

    # Основной цикл прослушки сообщений
    while True: # Обработка сообщений от клиента
        try: # Проверка на подключение к клиенту
            message = client_socket.recv(1024).decode()  # Получение сообщения от клиента
        except: # Если клиент отключён
            break # Выход из цикла

        # Запись сообщения в файл
        with open("server.log", "a") as file:
            file.write(f"{nickname} ({datetime.now().hour}:{datetime.now().minute}): {message}\n")
        print(f"{nickname} ({datetime.now().hour}:{datetime.now().minute}): {message}") # Вывод сообщения в консоль сервера

        # Отправка сообщения всем остальным клиентам
        for client in clients:
            with open("server.log", "r") as file:
                lines = file.readlines()
                last_messages = lines[-20:] if len(lines) > 20 else lines
                for message in last_messages:
                    client["socket"].send(message.encode())

    # Удаление клиента из списка
    clients.remove({"socket": client_socket, "address": client_address, "nickname": nickname})

# Серверный сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Создание сокета
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((server_host, server_port)) # Добавление данных для сервера сокета
server_socket.listen(MAX_CLIENTS) # Установка максимального числа клиентов
print("Server started on " + str(server_host) + ":" + str(server_port)) # Вывод информации о запуске сервера

while True: # Потоки для обработки клиентов
    client_socket, client_address = server_socket.accept() # Аргументы для создания сокета
    thread = threading.Thread(target=handle_client, args=(client_socket, client_address)) # Добавления сокета в поток
    thread.start() # Запуск потока