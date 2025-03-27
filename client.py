import socket
import os
import json
import cv2


def setup_cameras(num_cameras=2):
    """Инициализирует и настраивает камеры"""
    caps = []
    for i in range(num_cameras):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        if not cap.isOpened():
            print(f"Ошибка: не удалось открыть камеру {i}")
            continue
        caps.append(cap)
    return caps


def process_all_cameras(caps):
    """Обрабатывает все камеры и возвращает результаты"""
    images = []
    for i, cap in enumerate(caps):
        ret, frame = cap.read()
        if not ret:
            print(f"Ошибка чтения камеры {i}")
            continue
        # Сохраняем кадр в временный файл
        file_path = f"image_{i}.jpg"
        cv2.imwrite(file_path, frame)
        images.append(file_path)
    return images


def send_photos(file_path, ip_address, port):
    """Отправляет изображения на сервер и ожидает ответ в формате JSON."""
    with socket.socket() as s:
        s.connect((ip_address, port))

        if os.path.isfile(file_path):
            s.send(os.path.basename(file_path).encode())
            with open(file_path, "rb") as file:
                s.sendfile(file)
        else:
            print(f"Файл не найден: {file_path}")

        response = s.recv(4096).decode()
        return response


def main():
    # Настраиваем камеры
    caps = setup_cameras(num_cameras=1)

    # Обрабатываем камеры и получаем изображения
    photo_paths = process_all_cameras(caps)

    # Укажите IP-адрес и порт сервера
    ip_address = "26.72.52.1"
    port = 5001

    # Отправляем изображения и получаем ответ
    for file_path in photo_paths:
        response_data = send_photos(file_path, ip_address, port)
    response_data = json.loads(response_data)

    print("Ответ от сервера:", response_data)

    # Освобождаем ресурсы камер
    for cap in caps:
        cap.release()


if __name__ == "__main__":
    main()
