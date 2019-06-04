#!/usr/bin/env python3

#This script is adapted from the bluez sample script test/example-gatt-client

import dbus

try:
  from gi.repository import GObject
except ImportError:
  import gobject as GObject
import sys

from dbus.mainloop.glib import DBusGMainLoop

def get_bin_string(byteval):
    binstr = str(bin(byteval))
    binstr = binstr[2:]
    if len(binstr) < 8:
        binstr = (8-len(binstr))*'0' + binstr
    return binstr

class controller_state:
    #bits prior to 14 are for ???
    GYRO_X_START_BIT = 14
    GYRO_X_END_BIT = 26
    GYRO_Y_START_BIT = 27
    GYRO_Y_END_BIT = 39
    GYRO_Z_START_BIT = 40
    GYRO_Z_END_BIT = 52
    MAG_X_START_BIT = 53
    MAG_X_END_BIT = 65
    MAG_Y_START_BIT = 66
    MAG_Y_END_BIT = 78
    MAG_Z_START_BIT = 79
    MAG_Z_END_BIT = 91
    ACCEL_X_START_BIT = 92
    ACCEL_X_END_BIT = 104
    ACCEL_Y_START_BIT = 105
    ACCEL_Y_END_BIT = 117
    ACCEL_Z_START_BIT = 118
    ACCEL_Z_END_BIT = 130
    TOUCHPAD_X_POSITION_START_BIT = 131
    TOUCHPAD_X_POSITION_END_BIT = 138
    TOUCHPAD_Y_POSITION_START_BIT = 139
    TOUCHPAD_Y_POSITION_END_BIT = 146
    VOL_UP_BIT_POSITION = 147
    VOL_DOWN_BIT_POSITION = 148
    APP_BUTTON_BIT_POSITION = 149
    DAYDREAM_BUTTON_BIT_POSITION = 150
    TOUCHPAD_BUTTON_BIT_POSITION = 151
    #bits 152 through 160 are for ???.  They're not always zero so seemingly they do something.
    
    def split_bytearray(self,rawbytearray):
        self.overall_bit_string = ''
        for val in rawbytearray:
            self.overall_bit_string += get_bin_string(val)
            
        self.button_bits = self.overall_bit_string[147:152]
        self.touchpad_position_bits = self.overall_bit_string[131:147]
        
    def get_button_state(self, bit):
        if self.overall_bit_string[bit] == '0':
            return 'unpressed'
        else:
            return 'pressed'
        
    def get_touchpad_x_position(self):
        bitstr = self.overall_bit_string[self.TOUCHPAD_X_POSITION_START_BIT:self.TOUCHPAD_X_POSITION_END_BIT+1]
        return int(bitstr,2)
    
    def get_touchpad_y_position(self):
        bitstr = self.overall_bit_string[self.TOUCHPAD_Y_POSITION_START_BIT:self.TOUCHPAD_Y_POSITION_END_BIT+1]
        return int(bitstr,2)
    
    def get_accel_x_position(self):
        bitstr = self.overall_bit_string[self.ACCEL_X_START_BIT:self.ACCEL_X_END_BIT+1]
        return int(bitstr,2)
    
    def get_accel_y_position(self):
        bitstr = self.overall_bit_string[self.ACCEL_Y_START_BIT:self.ACCEL_Y_END_BIT+1]
        return int(bitstr,2)
    
    def get_accel_z_position(self):
        bitstr = self.overall_bit_string[self.ACCEL_Z_START_BIT:self.ACCEL_Z_END_BIT+1]
        return int(bitstr,2)
    
    def get_mag_x_position(self):
        bitstr = self.overall_bit_string[self.MAG_X_START_BIT:self.MAG_X_END_BIT+1]
        return int(bitstr,2)
    
    def get_mag_y_position(self):
        bitstr = self.overall_bit_string[self.MAG_Y_START_BIT:self.MAG_Y_END_BIT+1]
        return int(bitstr,2)
    
    def get_mag_z_position(self):
        bitstr = self.overall_bit_string[self.MAG_Z_START_BIT:self.MAG_Z_START_BIT+1]
        return int(bitstr,2)
    
    def get_gyro_x_position(self):
        bitstr = self.overall_bit_string[self.GYRO_X_START_BIT:self.GYRO_X_END_BIT+1]
        return int(bitstr,2)
    
    def get_gyro_y_position(self):
        bitstr = self.overall_bit_string[self.GYRO_Y_START_BIT:self.GYRO_Y_END_BIT+1]
        return int(bitstr,2)
    
    def get_gyro_z_position(self):
        bitstr = self.overall_bit_string[self.GYRO_Z_START_BIT:self.GYRO_Z_END_BIT+1]
        return int(bitstr,2)
        
    def vol_up_pressed(self):
        return self.get_button_state(self.VOL_UP_BIT_POSITION)
        
    def vol_down_pressed(self):
        return self.get_button_state(self.VOL_DOWN_BIT_POSITION)
    
    def app_pressed(self):
        return self.get_button_state(self.APP_BUTTON_BIT_POSITION)
    
    def daydream_pressed(self):
        return self.get_button_state(self.DAYDREAM_BUTTON_BIT_POSITION)
    
    def touchpad_pressed(self):
        return self.get_button_state(self.TOUCHPAD_BUTTON_BIT_POSITION)
    
    def __init__(self, rawbytearray):
        self.split_bytearray(rawbytearray)
        self.vol_up = self.vol_up_pressed()
        self.vol_down = self.vol_down_pressed()
        self.app_button = self.app_pressed()
        self.daydream_button = self.daydream_pressed()
        self.touchpad_button = self.touchpad_pressed()
        self.touchpad_x_position = self.get_touchpad_x_position()
        self.touchpad_y_position = self.get_touchpad_y_position()
        
        #The accel values seem a bit fishy, z in particular, so my bit 
        #alignment may not be quite right
        self.accel_x_position = self.get_accel_x_position()
        self.accel_y_position = self.get_accel_y_position()
        self.accel_z_position = self.get_accel_z_position()
    
        #I have no clue how to properly vet mag values
        self.mag_x_position = self.get_mag_x_position()
        self.mag_y_position = self.get_mag_y_position()
        self.mag_z_position = self.get_mag_z_position()
        
        #The gyro values seem sort of sensible but I don't know how to
        #properly vet them
        self.gyro_x_position = self.get_gyro_x_position()
        self.gyro_y_position = self.get_gyro_y_position()
        self.gyro_z_position = self.get_gyro_z_position()
        
    def as_dict(self):
        dictee = {}
        dictee['buttons'] = {}
        dictee['buttons']['volup'] = self.vol_up
        dictee['buttons']['voldown'] = self.vol_down
        dictee['buttons']['app'] = self.app_button
        dictee['buttons']['daydream'] = self.daydream_button
        dictee['buttons']['touchpad'] = self.touchpad_button
        
        dictee['touchpad'] = {}
        dictee['touchpad']['x'] = self.touchpad_x_position
        dictee['touchpad']['y'] = self.touchpad_y_position
        
        dictee['accel'] = {}
        dictee['accel']['x'] = self.accel_x_position
        dictee['accel']['y'] = self.accel_y_position
        dictee['accel']['z'] = self.accel_z_position
        
        dictee['mag'] = {}
        dictee['mag']['x'] = self.mag_x_position
        dictee['mag']['y'] = self.mag_y_position
        dictee['mag']['z'] = self.mag_z_position
        
        dictee['gyro'] = {}
        dictee['gyro']['x'] = self.gyro_x_position
        dictee['gyro']['y'] = self.gyro_y_position
        dictee['gyro']['z'] = self.gyro_z_position
            
        return dictee  

class daydream_bluetooth:
    def __init__(self, eclass=None):
        #class responsible for emitting the controller data
        self.emitclass = eclass

        # Set up the main loop.
        DBusGMainLoop(set_as_default=True)
        self.bus = dbus.SystemBus()
        self.mainloop = GObject.MainLoop()

        self.BLUEZ_SERVICE_NAME = 'org.bluez'
        self.DBUS_OM_IFACE =      'org.freedesktop.DBus.ObjectManager'
        self.DBUS_PROP_IFACE =    'org.freedesktop.DBus.Properties'

        self.GATT_SERVICE_IFACE = 'org.bluez.GattService1'
        self.GATT_CHRC_IFACE =    'org.bluez.GattCharacteristic1'

        self.CONTROLLER_SERVICE_UUID = '0000fe55-0000-1000-8000-00805f9b34fb'
        self.CONTROLLER_DATA_UUID = '00000001-1000-1000-8000-00805f9b34fb'

        om = dbus.Interface(self.bus.get_object(self.BLUEZ_SERVICE_NAME, '/'), self.DBUS_OM_IFACE)
        om.connect_to_signal('InterfacesRemoved', self.interfaces_removed_cb)

        print('Getting objects...')
        objects = om.GetManagedObjects()
        chrcs = []

        # List characteristics found
        for path, interfaces in objects.items():
            if self.GATT_CHRC_IFACE not in interfaces.keys():
                continue
            chrcs.append(path)


        # The objects that we interact with.
        self.controller_service = None
        self.controller_chrc = None

        # List sevices found
        for path, interfaces in objects.items():
            if self.GATT_SERVICE_IFACE not in interfaces.keys():
                continue

            chrc_paths = [d for d in chrcs if d.startswith(path + "/")]

            if self.process_controller_service(path, chrc_paths):
                break

        if not self.controller_service:
            print('No Controller Service found')
            sys.exit(1)

        self.start_client()

        
    def generic_error_cb(self, error):
        print('D-Bus call failed: ' + str(error))
        self.mainloop.quit()

    
    def get_hex_string(self, byteval):
        hexstr = str(hex(byteval))
        hexstr = hexstr[2:]
        if len(hexstr) == 1:
            hexstr = '0' + hexstr
        
    def controller_changed_cb(self, iface, changed_props, invalidated_props):
        if iface != self.GATT_CHRC_IFACE:
            return

        if not len(changed_props):
            return

        value = changed_props.get('Value', None)
        if not value:
            return

        current_controller_state = controller_state(value)
        if self.emitclass:
            self.emitclass.emit(current_controller_state.as_dict())
        else:
            print(current_controller_state.as_dict())

    def controller_start_notify_cb(self):
        print('Controller notifications enabled')

    def start_client(self):
        controller_prop_iface = dbus.Interface(self.controller_chrc[0], self.DBUS_PROP_IFACE)
        controller_prop_iface.connect_to_signal("PropertiesChanged",
                                            self.controller_changed_cb)
    
        # Subscribe to Controller notifications.
        self.controller_chrc[0].StartNotify(reply_handler=self.controller_start_notify_cb,
                                    error_handler=self.generic_error_cb,
                                    dbus_interface=self.GATT_CHRC_IFACE)


    def process_chrc(self, chrc_path):
        chrc = self.bus.get_object(self.BLUEZ_SERVICE_NAME, chrc_path)
        chrc_props = chrc.GetAll(self.GATT_CHRC_IFACE,
                             dbus_interface=self.DBUS_PROP_IFACE)

        uuid = chrc_props['UUID']

        if uuid == self.CONTROLLER_DATA_UUID:
            self.controller_chrc = (chrc, chrc_props)
        else:
            print('Unrecognized characteristic: ' + uuid)

        return True


    def process_controller_service(self, service_path, chrc_paths):
        service = self.bus.get_object(self.BLUEZ_SERVICE_NAME, service_path)
        service_props = service.GetAll(self.GATT_SERVICE_IFACE,
                                    dbus_interface=self.DBUS_PROP_IFACE)

        uuid = service_props['UUID']

        if uuid != self.CONTROLLER_SERVICE_UUID:
            return False

        print('Controller Service found: ' + service_path)

        # Process the characteristics.
        for chrc_path in chrc_paths:
            self.process_chrc(chrc_path)

        self.controller_service = (service, service_props, service_path)

        return True


    def interfaces_removed_cb(self, object_path, interfaces):
        if not self.controller_service:
            return

        if object_path == self.controller_service[2]:
            print('Service was removed')
            self.mainloop.quit()

    def run(self):
        self.mainloop.run()

def main():
    bluecontroller = daydream_bluetooth()
    bluecontroller.run()
  

if __name__ == '__main__':
    main()
