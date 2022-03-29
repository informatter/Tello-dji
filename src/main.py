import socket
import threading
from tello import Tello


tello = Tello()
tello.connect()
tello.run_test()