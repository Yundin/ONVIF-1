from onvif import ONVIFCamera
from time import sleep

def move_continuous(ptz_service, token, speedX, speedY, speedZ, timeout) :
	print 'Moving with speed ' + str(speedX) + ';' + str(speedY) + ';' + str(speedZ)

	try :
		# creating ContinuousMove request
		continuousMoveRequest = ptz_service.create_type('ContinuousMove')
		continuousMoveRequest.ProfileToken = media_profile._token
		continuousMoveRequest.Velocity.PanTilt._x = speedX
		continuousMoveRequest.Velocity.PanTilt._y = speedY
		continuousMoveRequest.Velocity.Zoom._x = speedZ
		continuousMoveRequest.Timeout = timeout

		ptz_service.ContinuousMove(continuousMoveRequest)
		print 'ContinuousMove should be successful'
		return True
	except Exception as e:
		# ContinuousMove request causes error
		print 'ContinuousMove is not supported'
		return False

def get_new_value_from_pos(val) :
	if (val > 0.5) :
		return 0.5
	else :
		return -0.5

def get_new_value_from_speed(val) :
	return val + 0.3

def check_continuous_move(ptz_service, media_profile) :
	x = y = z = 0 # initial values will be changed if coordinates available
	coordinatesAvailable = True
	try :
		# getting position
		position = ptz_service.GetStatus({"ProfileToken" : media_profile._token}).Position
		print 'Coordinates:'
		x = position.PanTilt._x
		print 'x: ' + str(x)
		y = position.PanTilt._y
		print 'y: ' + str(y)
		zoom = position.Zoom._x
		print 'zoom: ' + str(zoom)
	except Exception as e:
		# GetStatus request causes error
		coordinatesAvailable = False
		print 'Coordinates are not supported'

	# picking correct speed
	speedX = get_new_value_from_pos(x)
	speedY = get_new_value_from_pos(y)
	speedZ = get_new_value_from_pos(zoom)
	if move_continuous(ptz_service, media_profile._token, speedX, speedY, speedZ, 2):
		# first attemp seems successful, waiting timeout
		sleep(2)
		# picking correct speed
		speedX = get_new_value_from_speed(speedX)
		speedY = get_new_value_from_speed(speedY)
		speedZ = get_new_value_from_speed(speedZ)
		if move_continuous(ptz_service, media_profile._token, speedX, speedY, speedZ, 2) :
			print 'Test passed'

print 'Connecting to camera'
mycam = ONVIFCamera('192.168.15.42', 80, 'admin', 'Supervisor', '/etc/onvif/wsdl')
print 'Connected'
# creating services
ptz_service = mycam.create_ptz_service()
media_service = mycam.create_media_service()
# getting profile
media_profile = media_service.GetProfiles()[0]

check_continuous_move(ptz_service, media_profile)