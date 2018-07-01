from fri3d import Badge

def datacb(msg):
    print("[{}] Data arrived from topic: {}, Message:\n".format(msg[0], msg[1]), msg[2])


b = Badge(datacb)

state = 0

# l = robot.legs()
# e = robot.eyes()

res = b.connect()
if not res:
    print("Unable to initialize the badge")
else:
    b.mqtt.subscribe('test')


# def move_forward_backward(value):
#     if value < 500:
#         # -- backward
#         if value < 200:
#             l.walk_forward()
#         else:
#             l.step_forward()
#
#     elif value > 522:
#         # -- forward
#         if value > 800:
#             l.walk_backward()
#         else:
#             l.step_backward()
#
#
# def move_left_right(value):
#     if value < 500:
#         l.turn_left()
#     elif value > 522:
#         l.turn_right()
#
#
# def shake_leg(left):
#     if left:
#         l.shake_left()
#     else:
#         l.shake_right()
#
#
# def say_hello(left):
#     if left:
#         l.say_hello_left()
#     else:
#         l.say_hello_right()
#
#
# def reset_legs():
#     l.reset()
