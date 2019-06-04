import evdev

device = evdev.InputDevice('/dev/input/event15')

print(device.capabilities(verbose=True))
