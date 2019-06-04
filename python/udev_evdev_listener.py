import asyncio
from evdev import InputDevice, categorize, ecodes

dev = InputDevice('/dev/input/event15')

VOLUP = ecodes.BTN_0
VOLDOWN = ecodes.BTN_1
APP = ecodes.BTN_2
DAYDREAM = ecodes.BTN_3
TOUCHPAD = ecodes.BTN_4

def print_event(ev):
    prepend = ''
    
    if ev.type == ecodes.EV_KEY:
        if ev.code == VOLUP:
            prepend = 'volume up: '
        elif ev.code == VOLDOWN:
            prepend = 'volume down: '
        elif ev.code == APP:
            prepend = 'app button: '
        elif ev.code == DAYDREAM:
            prepend = 'daydream button: '
        elif ev.code == TOUCHPAD: 
            prepend = 'touchpad button: '
        else:
            prepend = 'unknown key: '
            
        print(prepend, ev.value)
    
async def helper(dev):
    async for ev in dev.async_read_loop():
        print_event(ev)
    
loop = asyncio.get_event_loop()
loop.run_until_complete(helper(dev))
