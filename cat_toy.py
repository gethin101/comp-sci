from machine import Pin, PWM
from time import sleep, ticks_us, ticks_diff

toy_motor = PWM(Pin(15))
toy_motor.freq(50)

def move_toy(angle):
    duty = int(1800 + (angle / 180) * 6200)
    toy_motor.duty_u16(duty)

trigger = Pin(2, Pin.OUT)
echo = Pin(3, Pin.IN)

def get_distance():
    trigger.low()
    sleep(0.000002)

    trigger.high()
    sleep(0.00001)
    trigger.low()

    while echo.value() == 0:
        start_time = ticks_us()

    while echo.value() == 1:
        end_time = ticks_us()

    travel_time = ticks_diff(end_time, start_time)
    return travel_time * 0.0343 / 2


while True:

    distance = get_distance()

    if distance < 15:

        print("\nCat detected:", round(distance, 1), "cm")

        for movement in range(5):
            move_toy(0)
            sleep(1)

            move_toy(180)
            sleep(1)

        move_toy(0)

    else:
        move_toy(90)
        sleep(0.2)
