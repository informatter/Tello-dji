TELLO_IP_ADRESS ='192.168.10.1'

# The port number Tello uses to receive
# commands and send responses
TELLO_RECEIVE_PORT_NUM = 8889

# The port number Tello uses to 
# send state information
TELLO_SEND_STATE_PORT_NUM = 8890

# The port number Tello uses to 
# send a video stream if video
# is enabled.
TELLO_SEND_VIDEO_STREAM_PORT_NUM = 1111

# The time in seconds a command
# will abort if a response was not received
RESPONSE_TIMEOUT = 7 #seconds

# The number of times a command
# can try executing 
MAX_RETRY_COMMAND_COUNT = 3

# The time interval in seconds to
# wait between commands
COMMAND_WAITING_TIME = 0.5