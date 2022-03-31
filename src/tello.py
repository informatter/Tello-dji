
from dis import Instruction
import threading 
import socket

# 
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
        self.counter = 0

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
        while self.can_run: 
            try:
                data, server = self.trello_socket.recvfrom(1518)
                message_from_trello = data.decode(encoding="utf-8")
                print("Trello says: %s" % message_from_trello)
                isBattery = message_from_trello.isnumeric()
                if(isBattery):
                    if(int(message_from_trello) <=15):
                        print("Trello says: My battery is below 15%, I will start landing...")
                        self.land()
            except Exception:
                print ("An error occured while hearing back from Trello ):")
                self.can_run = False
                break

    def __send_command(self,command):
        command = command.encode(encoding="utf-8") 
        self.trello_socket.sendto(command, self.address)


    # Terminates the connection with the Drone.
    def disconnect(self):
        self.trello_socket.close()
        self.can_run = False
    
    # Drone auto- takes off.
    def take_off(self):
        try:
            command = "takeoff"
            # self.__send_command(self,command)
            command = command.encode(encoding="utf-8") 
            self.trello_socket.sendto(command, self.address)
            
        except socket.error as e:
            print("Error taking off: %s" % e)

      # Lands the drone in the ground.
    def land(self):
        command = 'land'
        command = command.encode(encoding="utf-8") 
        self.log = self.trello_socket.sendto(command, self.address)

    # Moves the drone x cm's to the right.
    # "x" should be between 20 - 500 cm
    def move_right(self,x):
        command = 'left ' + str(x)
        command = command.encode(encoding="utf-8") 
        self.log = self.trello_socket.sendto(command, self.address)

    # Moves the drone x cm's to the left.
    # "x" should be between 20 - 500 cm.
    def move_left(self,x):
        command = 'left ' + str(x)
        command = command.encode(encoding="utf-8") 
        self.trello_socket.sendto(command, self.address)

     # Moves the drone x cm's forward.
     # "x" should be between 20 - 500 cm.
    def move_forward(self,x):
        command = 'forward ' + str(x)
        command = command.encode(encoding="utf-8") 
        self.log = self.trello_socket.sendto(command, self.address)

    def move_back(self,x):
        command = 'back ' + str(x)
        command = command.encode(encoding="utf-8") 
        self.log = self.trello_socket.sendto(command, self.address)

    def move_up(self,x):
        command = 'up ' + str(x)
        command = command.encode(encoding="utf-8") 
        self.log = self.trello_socket.sendto(command, self.address)
    
    def move_down(self,x):
        command = 'down ' + str(x)
        command = command.encode(encoding="utf-8") 
        self.log = self.trello_socket.sendto(command, self.address)
    
    def move_left(self,x):
        command = 'left ' + str(x)
        command = command.encode(encoding="utf-8") 
        self.log = self.trello_socket.sendto(command, self.address)

    def move_right(self,x):
        command = 'right ' + str(x)
        command = command.encode(encoding="utf-8") 
        self.log = self.trello_socket.sendto(command, self.address)

    def rotate(self,x):
        command = 'cw ' + str(x)
        command = command.encode(encoding="utf-8") 
        self.log = self.trello_socket.sendto(command, self.address)

    def get_life(self):
        command = 'battery?'
        command = command.encode(encoding="utf-8") 
        self.log = self.trello_socket.sendto(command, self.address)

    def start_video_stream(self):
          command = 'streamon'
          command = command.encode(encoding="utf-8") 
          self.log = self.trello_socket.sendto(command, self.address)


    def run_test(self):
        while self.can_run: 
            try:
                intruction = input("")
                if not input:break  

                if(intruction =='W'):
                    self.move_forward(80)
                if(intruction == 'S'):
                    self.move_back(80)
                if(intruction == 'T'):
                    self.take_off()
                if(intruction == 'L'):
                    self.land()
                if(intruction == 'D'):
                    self.move_right(80)
                if(intruction == 'A'):
                    self.move_left(80)
                if(intruction == 'R'):
                    self.rotate(50)
                if(intruction == 'H'):
                    self.move_down(20)
                if(intruction == 'Y'):
                    self.move_up(20)
                if(intruction == 'B'):
                    self.get_life()
                if(intruction == 'V'):
                    self.start_video_stream()
                
                if(self.counter<800):
                    self.counter+=1

                if(self.counter>=800):
                    print("Trello says: checking my health")
                    self.get_life()
                    self.counter =0

                

                if 'end' in intruction:
                    self.disconnect()
                    print ('Tello disconnected')
                    break
            except:
                self.disconnect() 
                break
        if(self.can_run is False): self.disconnect() 

