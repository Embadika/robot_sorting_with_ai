import cv2

# Путь видео файла
VIDEO_PATH = '0001-18000.avi'
# Путь к папке для хранения изображений
IMAGES_FOLDER_PATH = 'C:/Users/embad/Desktop/Diplom/IMAGES'
# Констнта, определяющая, сколько кадров будем пропускать
SHOTS = 30

# Инициализируем класс захвата и работы с видео
video_capture = cv2.VideoCapture(VIDEO_PATH)

# Счетчик сохраненных изображений
images_created = 0
# Счетчик считанных с видео кадров
shots_now = 0
# Переменная, обозначающая успешность считывания данных с видео
# Станет False когда видео закончится
success = True

# Цикл для получения всех кадров видео
while success:
    # Получаем состояние считывания данных и кадр
    success, image = video_capture.read()
    # Если текущий по счету кадр делится на количество кадров, которое мы пропускаем
    # без остатка, то будем сохранять изображение
    if shots_now % SHOTS == 0:
        # Сохраняем изображение в папку
        cv2.imwrite(f'IMAGES/image_{images_created}.jpg', image)
        # Увеличиваем счетчик созданных изображений
        images_created += 1
    # Увеличиваем счетчик прочитанных изображений
    shots_now += 1

# выводим информацию о количестве собранных изображений
print(f'End of creating dataset. Total images: {images_created}')
