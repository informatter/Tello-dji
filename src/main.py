
from tello import Tello

tello = Tello()
tello.connect()
tello.take_off()
tello.move_forward(100)
tello.rotate(360)
tello.rotate(360*0.15)
tello.flip_back()
#tello.move_up(100)
tello.move_right(50)
tello.move_left(100)
tello.flip_back()
tello.flip_front()
tello.flip_front()
tello.flip_left()
tello.flip_right()
tello.rotate(360)
tello.land()

