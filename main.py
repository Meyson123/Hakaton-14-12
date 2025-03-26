from pyA20.gpio import gpio
from pyA20.gpio import port
    # Инициализация GPIO
gpio.init()

# Определите порты для управления двигателем
motor1_pin1 = port.PA6  # Укажите правильные порты
motor1_pin2 = port.PA7

# Настройка портов как выходы
gpio.setcfg(motor1_pin1, gpio.OUTPUT)
gpio.setcfg(motor1_pin2, gpio.OUTPUT)

def motor_forward():
    gpio.output(motor1_pin1, gpio.HIGH)
    gpio.output(motor1_pin2, gpio.LOW)

def motor_backward():
    gpio.output(motor1_pin1, gpio.LOW)
    gpio.output(motor1_pin2, gpio.HIGH)

def motor_stop():
    gpio.output(motor1_pin1, gpio.LOW)
    gpio.output(motor1_pin2, gpio.LOW)

try:
    while True:
        command = input("Введите команду (f - вперед, b - назад, s - стоп, q - выход): ").strip().lower()
        if command == 'f':
            motor_forward()
            print("Двигатель движется вперед")
        elif command == 'b':
            motor_backward()
            print("Двигатель движется назад")
        elif command == 's':
            motor_stop()
            print("Двигатель остановлен")
        elif command == 'q':
            motor_stop()
            break
        else:
            print("Неверная команда")

except KeyboardInterrupt:
    motor_stop()

finally:
    gpio.cleanup()

