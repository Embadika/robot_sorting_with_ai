import cv2
import getpass
import time
import socket
import supervision as sv
import Stacker
import numpy as np
from inference import get_model

model = get_model(model_id='microcontrollersdetection/2',
                  api_key='uWNrYRoWIawm9sfiIfYY')

VIDEO_PATH = 'C:/Users/embad/Desktop/Diplom/0001-18000.avi'
ONE_PIXEL_LEN = 0.04
CONV_SPEED = 40

video_capture = cv2.VideoCapture(VIDEO_PATH)
label_annotator = sv.LabelAnnotator(text_color=sv.Color.BLACK)
bounding_box_annotator = sv.BoundingBoxAnnotator()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('', 8000)
print('Старт сервера на {} порт {}'.format(*server_address))
sock.bind(server_address)

commutator = np.array([[1, 1, 1],
                       [1, 1, 1],
                       [1, 1, 1],
                       [1, 1, 1]])

iskra_uno = np.array([[1, 1],
                        [1, 1]])

iskra_nano = np.array([[1],
                         [1]])

iot = np.array([[1, 1, 1],
                     [1, 1, 1],
                     [1, 1, 1]])

tara_commutator = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0]])

tara_iskra_uno = np.array([[0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0]])

tara_iskra_nano = np.array([[0, 0, 0],
                              [0, 0, 0],
                              [0, 0, 0],
                              [0, 0, 0],
                              [0, 0, 0],
                              [0, 0, 0]])

tara_iot = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0]])

tara_commutator = Stacker.Stacker(tara_commutator)
tara_iskra_nano = Stacker.Stacker(tara_iskra_nano)
tara_iskra_uno = Stacker.Stacker(tara_iskra_uno)
tara_iot = Stacker.Stacker(tara_iot)

tars = {'Commutator': {'tara': tara_commutator, 'part': commutator},
        'IskraUno': {'tara': tara_iskra_uno, 'part': iskra_uno},
        'IskraNano': {'tara': tara_iskra_nano, 'part': iskra_nano},
        'IoT': {'tara': tara_iot, 'part': iot}}

eng_rus = {'Commutator':'Commutator', 'ASUS IoT':'IoT', 'ArduinoUno':'IskraUno', 'ArduinoNano':'IskraNano'}

def cutImage(image):
    image = image[:, 360:1510]
    return image


def getMiddlePoint(xyxy, classes):
    '''
    Функция определения центра объекта
    Входные данные:
    xyxy - двумерный массив, состоящий из координат левого верхнего и правого нижнего угла bounding box в следующем формате:
           x_min, y_min, x_max, y_max]
    classes - список классов, которые были определены на изображении (классы по индексам совпадают с их координатами в массиве xyxy)
    Выходные данные:
    middle_points - двумерный список, содержащий в себе координаты центральных точек объектов
    new_classes - новый список классов на изображении, из которого убраны объекты, не полностью вошедшие в кадр
    '''
    middle_points = []  # Массив центральных точек
    new_classes = []  # Массив классов
    # Итерация по массиву координат
    for ind, coord in enumerate(xyxy):
        # Если координаты касаются края изображения с или близко к ним на 10 пикселей или меньше
        # пропускаем координату и класс
        if coord[1] <= 10 or coord[3] >= 1070:
            continue
        # Определяем центральную координату по x
        x_middle = int(coord[0] + (coord[2] - coord[0])/2)
        # Определяем центральную кординату по у
        y_middle = int(coord[1] + (coord[3] - coord[1])/2)
        # Добавляем класс и координаты в списки
        middle_points.append([x_middle, y_middle])
        new_classes.append(classes[ind])
    # Возвращаем данные
    return middle_points, new_classes


def transformPixelToCoords(points, ONE_PIXEL_LEN):
    '''
    Функция преобразования координат в пикселях камеры в координаты робота
    Входные данные:
    points - массив координат центральных точек на изображении
    ONE_PIXEL_LEN - константное значение, обозначающее количество миллиметров в одном пикселе
    Выходные данные:
    points_coords - массив координат объектов в системе робота
    '''
    # Определяем массив координат
    points_coords = []
    # Итерация по точкам в массиве
    for point in points:
        # Добавление в новый массив переведенных координат, округленных до 3 знаков после запятой
        points_coords.append(
            [round(point[0]*ONE_PIXEL_LEN, 3), round(point[1]*ONE_PIXEL_LEN, 3)])
    # Возвращаем данные
    return points_coords


def sendSignalToRobot(points_coords, classes, preparing_time, CONV_SPEED):
    points_x_classses = []
    for ind, point in enumerate(points_coords):
        points_x_classses.append({'class': classes[ind], 'point': point})
    if len(points_coords) == 0:
        print('Нет деталей для сортировки')
        return
    points_x_classses.sort(
        key=lambda x: [x['point'][1], x['point'][0]], reverse=False)
    point_for_send = points_x_classses[0]
    point_for_send['point'][1] = point_for_send['point'][1] - \
        CONV_SPEED*preparing_time
    return point_for_send


def analyzeImage(image):
    time_now = time.time()
    cutted_image = cutImage(image)
    result = model.infer(cutted_image, confidence=0.5)[0]
    detections = sv.Detections.from_inference(result)
    detections.data['class_name'] = [eng_rus[i] for i in detections.data['class_name']]
    annotated_image = cutted_image.copy()
    annotated_image = bounding_box_annotator.annotate(
        scene=annotated_image, detections=detections)
    annotated_image = label_annotator.annotate(
        scene=annotated_image, detections=detections)
    coords = detections.xyxy
    classes = detections.data['class_name']
    middle_points, classes = getMiddlePoint(coords, classes)
    points_coords = transformPixelToCoords(middle_points, ONE_PIXEL_LEN)
    for point in middle_points:
        annotated_image = cv2.circle(
            annotated_image, point, radius=5, color=(0, 0, 255), thickness=-1)
    end_time = time.time() - time_now
    points_for_send = sendSignalToRobot(
        points_coords, classes, end_time, CONV_SPEED)
    return annotated_image, points_for_send


for _ in range(1000):
    success, image = video_capture.read()

success = True
close_flag = False
sock.listen(1)

# Бесконечный цикл работы сервера
while True:
    print('Ожидаем соединения...')
    # Подключаем клиента
    connection, client_address = sock.accept()
    try:
        print(f'Подкючено к: {client_address}')
        
        while success:
            success, image = video_capture.read()
            data = connection.recv(16)
            if len(data) > 0:
                if data.decode() == 'Close':
                    close_flag = True
                    mes = 'Close'
                    connection.sendall(str(mes).encode())
                    break
                print(f'Получено: {data.decode()}')
                if data.decode() in tars.keys():
                    tars[data.decode()]['tara'].pickUp(1)
                    print(f'Тара {data.decode()} обновлена')
                    mes = f'Тара {data.decode()} обновлена'
                    connection.sendall(str(mes).encode())
                    continue
                annotated_image, points_for_send = analyzeImage(image)
                res, _ = tars[points_for_send['class']]['tara'].place(
                    tars[points_for_send['class']]['part'])
                if not res:
                    print('Тара {} переполнена'.format(
                        points_for_send['class']))
                    mes = 'Тара {} переполнена'.format(
                        points_for_send['class'])
                    connection.sendall(mes.encode())
                    continue
                print('Отправлен сигнал на робота с координатами: x - {}, y - {}, класс - {}'.format(round(points_for_send['point'][0], 3),
                                                                                                     round(
                                                                                                         points_for_send['point'][1], 3),
                                                                                                     points_for_send['class']))

                connection.sendall(str(points_for_send).encode())
            cv2.imshow('YOLOv9 detection', annotated_image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        if close_flag:
            break
    finally:
        connection.close()


video_capture.release()
cv2.destroyAllWindows()
