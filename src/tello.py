
import threading 
import socket
import sys
import time

class Tello:

    def __init__(self):
        self.host = ''
        self.port = 9000
        self.client_machine = (self.host,self.port)
        self.trello_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.log =''
        self.address = ('192.168.10.1', 8889)
        self.receiving_thread = None
        self.can_run = True

    def connect(self):
        try:
            self.trello_socket.bind(self.client_machine)
            skd_state = "command"
            skd_state = skd_state.encode(encoding="utf-8") 
            self.log = self.trello_socket.sendto(skd_state, self.address)
        except socket.error as e:
            print("Error creating socket: %s" % e)
    
    def listen_to_tello(self):
        self.receiving_thread = threading.Thread(target = self.__receive_from_tello)
        self.receiving_thread.start()

    def __receive_from_tello(self):
        count = 0
        while True: 
            try:
                data, server = self.trello_socket.recvfrom(1518)
                print("Trello says: %s" % data.decode(encoding="utf-8"))
            except Exception:
                print ("An error occured while hearing back from Trello ):")
                self.can_run = False
                break

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
            
        except socket.error as e:
            print("Error taking off: %s" % e)

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
        # print("Moved forward by: %s" % x +" cm")
        print(command)

    def move_back(self,x):
        command = 'back ' + str(x)
        command = command.encode(encoding="utf-8") 
        self.log = self.trello_socket.sendto(command, self.address)

    def run_test(self):
        while self.can_run: 
            try:
                msg = input("")
                if not msg:break  

                # if(msg =='W'):
                #     self.move_forward(80)
                # if(msg == 'S'):
                #     self.move_back(50)
                # if(msg == 'T'):
                #     self.take_off()
                # if(msg == 'L'):
                #     self.land()

                if 'end' in msg:
                    self.disconnect()
                    print ('Tello disconnected')
                    break

                # Send data
                msg = msg.encode(encoding="utf-8") 
                sent = self.trello_socket.sendto(msg, self.address)
                # print("Command sent to Trello: %s" % sent)
            # except KeyboardInterrupt:
            #     print ('\n . . .\n')
            #     self.disconnect()   
            #     break
            except:
                self.disconnect() 
                break
        if(self.can_run is False): self.disconnect() 

