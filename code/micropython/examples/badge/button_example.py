from fri3d import badge

# -- add a handler when the first button is pressed or released
badge.btn_0().on_press(lambda: print("BTN 0 Pressed"))
badge.btn_0().on_release(lambda: print("BTN 0 Released"))

# -- add a handler when the second button is pressed or released
badge.btn_1().on_press(lambda: print("BTN 1 Pressed"))
badge.btn_1().on_release(lambda: print("BTN 1 Released"))
