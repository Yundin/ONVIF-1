from onvif import ONVIFCamera
from time import sleep

def move_abs(ptz_service, token, newX, newY, newZ, coordinatesAvailable) :
	print 'Moving to ' + str(newX) + ';' + str(newY) + ';' + str(newZ)

	try :
		# creating AbsoluteMove request
		absoluteMoveRequest = ptz_service.create_type('AbsoluteMove')
		absoluteMoveRequest.ProfileToken = media_profile._token
		absoluteMoveRequest.Position.PanTilt._x = newX
		absoluteMoveRequest.Position.PanTilt._y = newY
		absoluteMoveRequest.Position.Zoom._x = newZ

		ptz_service.AbsoluteMove(absoluteMoveRequest)
		print 'AbsoluteMove should be successful'
		if coordinatesAvailable :
			# only when coordinates are available checking position a few seconds later
			sleep(10)
			position = ptz_service.GetStatus({"ProfileToken" : media_profile._token}).Position
			x = position.PanTilt._x
			y = position.PanTilt._y
			z = position.Zoom._x
			if (newX == x and newY == y and newZ == z) :
				# position matches expected
				print 'Coordinates changed'
				return True
			else :
				# position not matches expected
				print 'New coordinates are ' + str(x) + ';' + str(y) + ';' + str(z)
				return False
		else :
			return True
	except Exception as e:
		# AbsoluteMove request causes error
		print 'AbsoluteMove is not supported'
		return False

def get_new_pos_value_from(val) :
	if (val + 0.1 > 1) :
		return val - 0.1
	else :
		return val + 0.1
def get_new_zoom_value_from(val) :
	if (val == 1.0) :
		return 0.0
	else :
		return 1.0

def check_absolute_move(ptz_service, media_profile) :
	x = y = z = 0 # initial value will be changed if coordinates available
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

	# picking correct coordinates
	newX = get_new_pos_value_from(x)
	newY = get_new_pos_value_from(y)
	newZ = get_new_zoom_value_from(zoom)
	if move_abs(ptz_service, media_profile._token, newX, newY, newZ, coordinatesAvailable):
		# first attemp was successful
		# picking correct coordinates
		newX = get_new_pos_value_from(newX)
		newY = get_new_pos_value_from(newY)
		newZ = get_new_zoom_value_from(newZ)
		if move_abs(ptz_service, media_profile._token, newX, newY, newZ, coordinatesAvailable) :
			print 'Test passed'
		else :
			print 'Coordinates not matches'
	else :
		print 'Coordinates not matches'

print 'Connecting to camera'
mycam = ONVIFCamera('192.168.15.42', 80, 'admin', 'Supervisor', '/etc/onvif/wsdl')
print 'Connected'
# creating services
ptz_service = mycam.create_ptz_service()
media_service = mycam.create_media_service()
# getting profile
media_profile = media_service.GetProfiles()[0]

check_absolute_move(ptz_service, media_profile)