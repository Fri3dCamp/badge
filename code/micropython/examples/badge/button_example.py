from fri3d import Badge

b = Badge()

# -- add a handler when the first button is pressed or released
b.button_0.on_press(lambda: print("BTN 0 Pressed"))
b.button_0.on_release(lambda: print("BTN 0 Released"))

# -- add a handler when the second button is pressed or released
b.button_1.on_press(lambda: print("BTN 1 Pressed"))
b.button_1.on_release(lambda: print("BTN 1 Released"))
