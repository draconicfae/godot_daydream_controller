extends Node2D


#preload nodes for the controller button value labels
onready var volupvalnode = get_node("VolUpValue")
onready var voldownvalnode = get_node("VolDownValue")
onready var appbuttonvalnode = get_node("AppButtonValue")
onready var daydreambuttonvalnode = get_node("DaydreamButtonValue")
onready var touchbuttonvalnode = get_node("TouchButtonValue")

#preload nodes for the gyro value labels
onready var gyroxvalnode = get_node("GyroXValue")
onready var gyroyvalnode = get_node("GyroYValue")
onready var gyrozvalnode = get_node("GyroZValue")

#preload nodes for the accel value labels
onready var accelxvalnode = get_node("AccelXValue")
onready var accelyvalnode = get_node("AccelYValue")
onready var accelzvalnode = get_node("AccelZValue")

#preload nodes for the mag value labels
onready var magxvalnode = get_node("MagXValue")
onready var magyvalnode = get_node("MagYValue")
onready var magzvalnode = get_node("MagZValue")

#preload nodes for the touch location value labels
onready var touchxvalnode = get_node("TouchXValue")
onready var touchyvalnode = get_node("TouchYValue")

var joy_mapped = false

var volupval = ''
func set_volup(val):
	if val != volupval:
		volupvalnode.text = val
		volupval = val
	
var voldownval = ''
func set_voldown(val):
	if val != voldownval:
		voldownvalnode.text = val
		voldownval = val
		
var appbuttonval = ''
func set_appbutton(val):
	if val != appbuttonval:
		appbuttonvalnode.text = val
		appbuttonval = val
		
var touchbuttonval = ''
func set_touchbutton(val):
	if val != touchbuttonval:
		touchbuttonvalnode.text = val
		touchbuttonval = val
	
var daybuttonval = ''
func set_daybutton(val):
	if val != daybuttonval:
		daydreambuttonvalnode.text = val
		daybuttonval = val
	

func set_buttons(vals):
	set_volup(str(vals['volup']))
	set_voldown(str(vals['voldown']))
	set_appbutton(str(vals['app']))
	set_daybutton(str(vals['daydream']))
	set_touchbutton(str(vals['touchpad']))
	
	
class xyz:
	var x = 0.0
	var y = 0.0
	var z = 0.0
	
func set_xyz(xyznew, xyzold, xnode, ynode, znode):
	if xyzold.x != xyznew['x']:
		xnode.text = str(xyznew['x'])
		xyzold.x = xyznew['x']
		
	if xyzold.y != xyznew['y']:
		ynode.text = str(xyznew['y'])
		xyzold.y = xyznew['y']
		
	if xyzold.z != xyznew['z']:
		znode.text = str(xyznew['z'])
		xyzold.z = xyznew['z']
		
var gyroxyz = xyz.new()
func set_gyro(vals):
	set_xyz(vals, gyroxyz, gyroxvalnode, gyroyvalnode, gyrozvalnode)
		
var accelxyz = xyz.new()
func set_accel(vals):
	set_xyz(vals, accelxyz, accelxvalnode, accelyvalnode, accelzvalnode)

var magxyz = xyz.new()
func set_mag(vals):
	set_xyz(vals, magxyz, magxvalnode, magyvalnode, magzvalnode)

var touchx = 0.0
var touchy = 0.0
func set_touchxy(vals):
	if touchx != vals['x']:
		touchxvalnode.text = str(vals['x'])
		touchx = vals['x']
		
	if touchy != vals['y']:
		touchyvalnode.text = str(vals['y'])
		touchy = vals['y']
		
# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	if not joy_mapped:
		#a:b3 maps to volup; start:b4 maps to voldown; b:b5 maps to app button; x:b6 maps to daydream button; y:b7 maps to touchpad button
		Input.add_joy_mapping("03000000010000000100000003000000,Daydream Controller,a:b3,start:b4,b:b5,x:b6,y:b7,leftx:a0,lefty:a1,platform:Linux",true)

		joy_mapped = true

	var vals = {}
	vals['volup'] = Input.is_joy_button_pressed(0,0)
	vals['voldown'] = Input.is_joy_button_pressed(0,11)
	vals['app'] = Input.is_joy_button_pressed(0,1)
	vals['daydream'] = Input.is_joy_button_pressed(0,2)
	vals['touchpad'] = Input.is_joy_button_pressed(0,3)
	set_buttons(vals)
	
	var touchpad_coords = {}
	touchpad_coords['x'] = Input.get_joy_axis(0,0)
	touchpad_coords['y'] = Input.get_joy_axis(0,1)
	set_touchxy(touchpad_coords)