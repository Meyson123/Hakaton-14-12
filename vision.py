import cv2
import numpy as np

# Настройки цветов светодиодов (в формате HSV)
COLORS = {
    'красный': ([0, 150, 100], [10, 255, 255]),
    'зеленый': ([40, 50, 50], [90, 255, 255]),
    'синий': ([100, 150, 50], [140, 255, 255]),
    'желтый': ([20, 100, 100], [40, 255, 255])
}


def setup_cameras(num_cameras=2):
    """Инициализирует и настраивает камеры"""
    caps = []
    for i in range(num_cameras):
        cap = cv2.VideoCapture(i,cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        if not cap.isOpened():
            print(f"Ошибка: не удалось открыть камеру {i}")
            continue
        caps.append(cap)
        print(caps)
    return caps






    finally:
        # Освобождение ресурсов
        for cap in caps:
            cap.release()
        cv2.destroyAllWindows()


# Инициализация и запуск
if __name__ == "__main__":
    cameras = setup_cameras(2)
    # 2 камеры
    if cameras:
        main_loop(cameras)
    else:
        print("Не удалось инициализировать ни одной камеры")
