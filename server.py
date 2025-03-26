import socket
import cv2
import numpy as np
import os

COLORS = {
    'красный': ([0, 150, 100], [10, 255, 255]),
    'зеленый': ([40, 50, 50], [90, 255, 255]),
    'синий': ([100, 150, 50], [140, 255, 255]),
    'желтый': ([20, 100, 100], [40, 255, 255])
}

def start_server():
    """Запуск сервера для приема изображений."""
    server_socket = socket.socket()  # Создаем сокет
    server_socket.bind(('0.0.0.0', 5001))  # Связываем его с IP и портом
    server_socket.listen(1)  # Начинаем слушать входящие соединения
    print("Сервер запущен и ожидает подключения...")

    while True:
        conn, address = server_socket.accept()  # Принимаем соединение
        print("Подключен к: " + str(address))

        # Получаем имя файла
        file_name = conn.recv(1024).decode()
        print(f"Получаем файл: {file_name}")

        # Записываем полученный файл
        with open(file_name, "wb") as file:
            print("Начинаем запись файла...")
            while True:
                data = conn.recv(1024)
                if not data:
                    break  # Если нет данных, выходим из цикла
                file.write(data)  # Записываем данные в файл

        print("Файл успешно получен!")
        results = process_image(file_name)  # Обрабатываем изображение на наличие цветов
        print(results)

        # Отправляем результаты обратно клиенту
        conn.sendall(str(results).encode())
        print("Результаты отправлены клиенту!")

        conn.close()  # Закрываем соединение
        os.remove(file_name)  # Удаляем файл после обработки


def process_frame(frame):
    """Обрабатывает один кадр, детектирует светодиоды"""
    detected = []
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    for color_name, (lower, upper) in COLORS.items():
        mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
        mask = cv2.medianBlur(mask, 5)

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest) > 100:
                x, y, w, h = cv2.boundingRect(largest)
                center = (x + w // 2, y + h // 2)
                size = (w + h) // 2
                detected.append((color_name, center, size))

                # Рисуем маркеры на кадре
                cv2.circle(frame, center, size, (0, 255, 0), 2)
                cv2.putText(frame, color_name, (center[0] + size, center[1]),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    return detected

def process_image(file_name):
    """Обрабатывает изображение и возвращает результаты обнаружения цветов"""
    results = {}
    image = cv2.imread(file_name)

    if image is None:
        print("Ошибка открытия изображения")
        return results

    detected = process_frame(image)
    results['detected'] = detected  # Сохраняем результаты обнаружения

    return results

if __name__ == '__main__':
    start_server()  # Запускаем сервер
