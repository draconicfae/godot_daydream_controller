from evdev import UInput, AbsInfo, ecodes as e

class udev_evdev_emit:
    def __init__(self):
        print('initializing udev_evdev_emit')
        #several of these cap mappings are fake and just intended to ensure that Godot sees us as a valid controller
        #actual mappings: volup = BTN_0; voldown = BTN_1; app button = BTN_2; daydream button = BTN_3; touchpad button = BTN_4 
        cap = { e.EV_KEY : [e.BTN_A, e.BTN_THUMBL, e.BTN_TRIGGER, e.BTN_0, e.BTN_1, e.BTN_2, e.BTN_3, e.BTN_4], e.EV_ABS : [e.ABS_X, e.ABS_Y, e.ABS_HAT0X, e.ABS_GAS, e.ABS_RUDDER]}
        self.ui = UInput(cap, name="daydream controller", version=0x3)

    def pressed_to_int(self, data):
        if data == "pressed":
            return 1
        else:
            return 0
        
    def emit(self, data):
        self.ui.write(e.EV_KEY, e.BTN_0, self.pressed_to_int(data['buttons']['volup']))
        self.ui.write(e.EV_KEY, e.BTN_1, self.pressed_to_int(data['buttons']['voldown']))
        self.ui.write(e.EV_KEY, e.BTN_2, self.pressed_to_int(data['buttons']['app']))
        self.ui.write(e.EV_KEY, e.BTN_3, self.pressed_to_int(data['buttons']['daydream']))
        self.ui.write(e.EV_KEY, e.BTN_4, self.pressed_to_int(data['buttons']['touchpad']))
        self.ui.syn()
