import socket

# Создаем сокет
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Определяем адресс и порт сервера
server_address = ('localhost', 8000)
# Подключаемся к серверу
sock.connect(server_address)
print('Подключено к {} порт {}'.format(*server_address))

# Флаг обозначающий окончание работы
flag_end = False

while True:
    # Вводим сообщение, которое отправим на сервер
    mess = input('Введие сообщение: ')
    # Кодируем сообщение в байтовый вид
    message = mess.encode()
    try:
        # Пробуем послать сообщение
        sock.sendall(message)
        # Константы для отслеживания текущей длины сообщения
        # и максимальной длины
        ammount_recieved = 0
        ammount_expected = 20

        # Пока не превысили максимальную дилну сообщения
        while ammount_recieved < ammount_expected:
            # Получаем ответ от сервера
            data = sock.recv(1024)
            # Прибавляем к полученной длине длину ответа
            ammount_recieved += len(data)
            # Раскодируем сообщение сервера
            mess = data.decode()
            # Если сервер возвращает Close
            if mess == 'Close':
                # Активируем флаг окончания работы
                flag_end = True
                print('Закрываем сокет')
                # Закрваем сокет
                sock.close()
                break
            print(f'Получено: {data.decode()}')
        # Выходим из бесконесного цикла, если активирован флаг
        if flag_end:
            break
    except:
        # Если сервер не отвечает, то закрываем сокет
        print('Закрываем сокет')
        sock.close()
