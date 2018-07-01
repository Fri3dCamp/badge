from fri3d import Badge
from fri3d.kits.robot import Legs

LEFT = 'LEFT'
RIGHT = 'RIGHT'
FORWARD = 'FORWARD'
BACKWARD = 'BACKWARD'

RESET = 'RESET'
STEP = 'STEP'
SHAKE = 'SHAKE'
HELLO = 'HELLO'
TUNE = 'TUNE'


def on_legs_data(data):
    parts = data.split()

    if parts[0] == RESET:
        legs.reset()

    elif parts[0] == TUNE:
        if len(parts) != 4:
            print("bwek")
            return

        idx = int(parts[1])
        min = float(parts[2])
        max = float(parts[3])

        if idx < 0 or idx > 3:
            print("bwok")
            return

        legs.servos.tune(idx, min, max)
        print("tuned servo " + str(idx))

    else:
        if len(parts) <= 1:
            return

        if parts[0] == STEP:
            speed = 15
            if len(parts) == 3:
                speed = int(parts[2])

            if parts[1] == FORWARD:
                legs.step_forward(speed)
            elif parts[1] == BACKWARD:
                legs.step_backward(speed)
            elif parts[1] == LEFT:
                legs.turn_left(speed)
            elif parts[1] == RIGHT:
                legs.turn_right(speed)

        elif parts[0] == SHAKE:
            if parts[1] == LEFT:
                legs.shake_left()
            elif parts[1] == RIGHT:
                legs.shake_right()

        elif parts[0] == HELLO:
            if parts[1] == LEFT:
                legs.say_hello_left()
            elif parts[1] == RIGHT:
                legs.say_hello_right()


def on_eyes_data(data):
    """
    Handle eye commands

        PUPIL <x> <y> <eye_ids>
        BLINK <eye_ids>
        THINK
        RESET

    :param data:
    :return:
    """
    parts = data.split()

    if parts[0] == 'PUPIL':
        eye_ids = []
        if len(parts) == 4:
            eye_ids = [int(i) for i in parts[3].split(",")]

        print(eye_ids)

        b.eyes.pupil(int(parts[1]), int(parts[2]), *eye_ids)

    elif parts[0] == 'BLINK':
        eye_ids = []
        if len(parts) == 2:
            eye_ids = [int(i) for i in parts[1].split(",")]

        b.eyes.blink(*eye_ids)

    elif parts[0] == 'THINK':
        b.eyes.thinking()

    elif parts[0] == 'RESET':
        b.eyes.reset()


def on_data(msg):
    if msg[1] == PREFIX + "/eyes":
        on_eyes_data(msg[2])
    elif msg[1] == PREFIX + "/legs":
        on_legs_data(msg[2])
    else:
        print("[{}] Data arrived from topic: {}, Message:\n".format(msg[0], msg[1]), msg[2])


b = Badge(data_cb=on_data, enable_eyes=True)
legs = Legs()

PREFIX = 'fri3d/badge/' + b.id

res = b.connect()
if not res:
    print("Unable to initialize the badge")
else:
    b.mqtt.subscribe(PREFIX + "/eyes")
    b.mqtt.subscribe(PREFIX + "/legs")
