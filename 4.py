from onvif import ONVIFCamera
from time import sleep

def check_focus_move(imaging_service, media_profile) :
	videoSourceToken = media_profile.VideoSourceConfiguration.SourceToken
	focusValeAvailable = True
	focusVal = 0 # initial value will be changed if status available
	try:
		focusVal = imaging_service.GetStatus({"VideoSourceToken" : videoSourceToken}).FocusStatus20.Position
	except Exception as e:
		# GetStatus request causes error
		print 'Focus value is unreachable'
		focusValeAvailable = False

	# setting AutoFocusMode to MANUAL
	try:
		# getting existing imaging settings
		imagingSettings = imaging_service.GetImagingSettings({"VideoSourceToken" : videoSourceToken})
		# creating SetImagingSettings request
		setImagingSettingsRequest = imaging_service.create_type('SetImagingSettings')
		setImagingSettingsRequest.VideoSourceToken = videoSourceToken
		setImagingSettingsRequest.ImagingSettings = imagingSettings
		setImagingSettingsRequest.ImagingSettings.Focus.AutoFocusMode = 'MANUAL'

		imaging_service.SetImagingSettings(setImagingSettingsRequest)
		print 'AutoFocusMode is set on manual'
	except Exception as e:
		# GetImagingSettings request causes error
		print 'AutoFocusMode cannot be set on manual'

	# checking absolute focus move
	try:
		# picking correct value
		if (focusVal + 0.1 <= 1) :
			newVal = focusVal + 0.1
		else :
			newVal = focusVal - 0.1
		# creating move request
		focusMoveRequest = imaging_service.create_type('Move')
		focusMoveRequest.VideoSourceToken = videoSourceToken
		focusMoveRequest.Focus.Absolute.Position = newVal
		focusMoveRequest.Focus.Absolute.Speed = 1

		imaging_service.Move(focusMoveRequest)
		print 'Absolute focus move should be successful'
		if focusValeAvailable :
			# only when focus is available checking value a few seconds later
			sleep(4)
			newFocusVal = imaging_service.GetStatus({"VideoSourceToken" : videoSourceToken}).FocusStatus20.Position
			if focusVal == newFocusVal :
				print 'Focus value is unchanged'
			else :
				print 'Focus value is changed and now ' + str(newFocusVal)
	except Exception as e:
		# Move request causes error
		print 'Absolute focus move is not supported'

	# checking relative focus move
	try:
		# picking correct value
		if (focusVal + 0.1 <= 1) :
			newVal = 0.1
		else :
			newVal = -0.1
		# creating move request
		focusMoveRequest = imaging_service.create_type('Move')
		focusMoveRequest.VideoSourceToken = videoSourceToken
		focusMoveRequest.Focus.Relative.Distance = newVal
		focusMoveRequest.Focus.Relative.Speed = 1

		imaging_service.Move(focusMoveRequest)
		print 'Relative focus move should be successful'
		if focusValeAvailable :
			sleep(4)
			newFocusVal = imaging_service.GetStatus({"VideoSourceToken" : videoSourceToken}).FocusStatus20.Position
			if focusVal == newFocusVal :
				print 'Focus value is unchanged'
			else :
				print 'Focus value is changed and now ' + str(newFocusVal)
	except Exception as e:
		# Move request causes error
		print 'Relative focus move is not supported'

	# checking continuous focus move
	try:
		# picking correct value
		if (focusVal + 0.1 <= 1) :
			newVal = 1
		else :
			newVal = -1
		# creating move request
		focusMoveRequest = imaging_service.create_type('Move')
		focusMoveRequest.VideoSourceToken = videoSourceToken
		focusMoveRequest.Focus.Continuous.Speed = newVal

		imaging_service.Move(focusMoveRequest)
		print 'Continuous focus move should be successful'
		if focusValeAvailable :
			sleep(4)
			newFocusVal = imaging_service.GetStatus({"VideoSourceToken" : videoSourceToken}).FocusStatus20.Position
			if focusVal == newFocusVal :
				print 'Focus value is unchanged'
			else :
				print 'Focus value is changed and now ' + str(newFocusVal)
	except Exception as e:
		# Move request causes error
		print 'Continuous focus move is not supported'

print 'Connecting to camera'
mycam = ONVIFCamera('192.168.15.42', 80, 'admin', 'Supervisor', '/etc/onvif/wsdl')
print 'Connected'
# creating services
media_service = mycam.create_media_service()
imaging_service = mycam.create_imaging_service()
# getting profile
media_profile = media_service.GetProfiles()[0]

check_focus_move(imaging_service, media_profile)