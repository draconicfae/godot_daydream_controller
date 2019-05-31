extends Node2D

# Declare member variables here. Examples:
# var a = 2
# var b = "text"

var done
var socket

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

# Called when the node enters the scene tree for the first time.
func _ready():
	done=false
	var port=50007
	var addr='127.0.0.1'
	
	socket=PacketPeerUDP.new()

	if(socket.listen(port,addr) != OK):
		print("an error occurred listening on port " + str(port))
		done=true
	else:
		print("Listening on port " + str(port) + " on " + addr)

func is_pressed(val):
	return val == 'pressed'
	
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
	set_volup(vals['volup'])
	set_voldown(vals['voldown'])
	set_appbutton(vals['app'])
	set_daybutton(vals['daydream'])
	set_touchbutton(vals['touchpad'])
	
	
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
	if (done!=true):
		if (socket.get_available_packet_count() > 0):
			var data = socket.get_packet().get_string_from_ascii()
			if (data=='quit'):
				done=true
			else:
				#print enough of the string to see whether volup is pressed
				#uncomment this and leave the other extraction approaches
				#commented out to see how fast it can echo without any 
				#fancy processing
				#print(data.substr(0,32))
				
				#extract the json and update the button labels
				var jsonval = parse_json(data)
				set_buttons(jsonval['buttons'])
				set_gyro(jsonval['gyro'])
				set_mag(jsonval['mag'])
				set_accel(jsonval['accel'])
				set_touchxy(jsonval['touchpad'])
				
	
	if done == true:
		socket.close()
		print("no longer listening for udp packets")
