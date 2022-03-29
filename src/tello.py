
import threading 
import socket
import sys
import time

class Tello:

    def __init__(self):
        self.host = ''
        self.port = 9000
        self.locaddr = (self.host,self.port)
        self.trello_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.log =''
        self.address = ('192.168.10.1', 8889)

    def connect(self):
        try:
            self.trello_socket.bind(self.locaddr)

            skd_state = "Command"
            skd_state = skd_state.encode(encoding="utf-8") 
            self.log = self.trello_socket.sendto(skd_state, self.address)
            print('connected')
        except:
            print(self.log)

    # Terminates the connection with the Drone.
    def disconnect(self):
        self.trello_socket.close()

    # Moves the drone x cm's to the left.
    # "x" should be between 20 - 500 cm.
    def move_left(self,x):
        command = 'left ' + str(x)
        command = command.encode(encoding="utf-8") 
        self.trello_socket.sendto(command, self.address)
    
    # Drone auto- takes off.
    def take_off(self):
        try:
            command = "takeoff"
            command = command.encode(encoding="utf-8") 
            self.log = self.log = self.trello_socket.sendto(command, self.address)
            print("taking off")
            print(self.log)
        except:
            print("failed")

    # Moves the drone x cm's to the right.
    # "x" should be between 20 - 500 cm
    def move_right(self,x):
        command = 'left ' + str(x)
        command = command.encode(encoding="utf-8") 
        self.log = self.trello_socket.sendto(command, self.address)

    # Lands the drone in the ground.
    def land(self):
        command = 'land'
        command = command.encode(encoding="utf-8") 
        self.log = self.trello_socket.sendto(command, self.address)

    def move_forward(self,x):
        command = 'forward ' + str(x)
        command = command.encode(encoding="utf-8") 
        self.log = self.trello_socket.sendto(command, self.address)

    def run_test(self):
        while True: 

            # end -- quit demo
            try:
                msg = input("")

                print(msg) 

                if not msg:
                    break  

                if 'end' in msg:
                    print ('...')
                    self.trello_socket.close()  
                    break

                # Send data
                msg = msg.encode(encoding="utf-8") 
                sent = self.trello_socket.sendto(msg, self.address)
            except KeyboardInterrupt:
                print ('\n . . .\n')
                self.trello_socket.close()  
                break

