
from dis import Instruction
import threading 
import socket
import time
import logging


class Tello:


    TELLO_IP_ADRESS ='192.168.10.1'
    TELLO_PORT_NUM = 8889
    COMMAND_RETRY_COUNT = 10
    RESPONSE_TIMEOUT = 7 #seconds
    MAX_RETRY_COMMAND_COUNT = 3

    def __init__(self, client_machine_ip: str = ''):
       
        # self.port = 9000
        self.address = (Tello.TELLO_IP_ADRESS, Tello.TELLO_PORT_NUM)
        self.client_machine = (client_machine_ip,Tello.TELLO_PORT_NUM) #(self.client_machine_ip,self.port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.log =''
        self.receive_response_thread = None
        self.can_run = True
        self.counter = 0
        self.last_command_received_at = time.time()
        self.tello_responses =[]


    def connect(self):
        try:
            self.client_socket.bind(self.client_machine)
            skd_state = "command"
            skd_state = skd_state.encode(encoding="utf-8") 
            self.log = self.client_socket.sendto(skd_state, self.address)
        except socket.error as e:
            print("Error creating socket: %s" % e)
    
    def listen_to_tello(self):
        self.receive_response_thread = threading.Thread(target = self.__receive_response_from_tello)
        self.receive_response_thread.start()

    def __receive_response_from_tello(self):
        while True: 
            try:
                data, address = self.client_socket.recvfrom(1518)
                address = address[0]
                print('Data received from {} at client_socket'.format(address))
                if(address!=self.address): continue
                self.tello_responses.append(data)
            except Exception:
                print ("An error occured while hearing back from Trello ):")
                break

    def __try_send_control_command(self, command:str) -> str:

        delta_time = time.time() - self.last_command_received_at
        if delta_time < 0.1:
            time.sleep(delta_time)

        self.client_socket.sendto(command.encode('utf-8'), self.address)

        current_time = time.time()
       
        # If there are no responses, will check time out, if time
        # has exeeded, this method will abort.
        while not self.tello_responses:
            # aborts command if did not receive response back from Tello
            # after response timeout
            if time.time() - current_time > Tello.RESPONSE_TIMEOUT:
                error_message = "Aborting command '{}'. Did not receive a response after the timeout of {} seconds".format(command, Tello.RESPONSE_TIMEOUT)
                print( error_message)
                return error_message

            time.sleep(0.1)

        self.last_command_received_at = time.time()

        # returns latest response.
        first_response = self.tello_responses.pop(0)
        try:
            response = first_response.decode("utf-8")
        except UnicodeDecodeError as e:
            error_message = "Encountered an error while decoding response:{}".format(e)
            return error_message

        response = response.rstrip("\r\n")
        print("Response from command {}: '{}'".format(command, response))
        return response

    # Send a command which controls the behavior of Tello
    def send_action_command(self, command:str):
        response = "max retries exceeded"
        for i in range(0, Tello.MAX_RETRY_COMMAND_COUNT): # 3 = rmax etry count
            response = self.__try_send_control_command(command)
            if 'ok' in response.lower():return

            print("Command attempt #{} failed for command: '{}'".format(i, command))

        print("Max retries for command {} have exceeded".format(command))


    # Terminates the connection with the Drone.
    def disconnect(self):
        self.client_socket.close()
    
    # Drone auto- takes off.
    def take_off(self):
        self.send_action_command('takeoff')

      # Lands the drone in the ground.
    def land(self):
        self.send_action_command('land')

    # Moves the drone x cm's to the right.
    # "x" should be between 20 - 500 cm
    def move_right(self,x):
        command = 'left ' + str(x)
        command = command.encode(encoding="utf-8") 
        self.log = self.client_socket.sendto(command, self.address)

    # Moves the drone x cm's to the left.
    # "x" should be between 20 - 500 cm.
    def move_left(self,x):
        command = 'left ' + str(x)
        command = command.encode(encoding="utf-8") 
        self.client_socket.sendto(command, self.address)

     # Moves the drone x cm's forward.
     # "x" should be between 20 - 500 cm.
    def move_forward(self,x):
        command = 'forward ' + str(x)
        command = command.encode(encoding="utf-8") 
        self.log = self.client_socket.sendto(command, self.address)

    def move_back(self,x):
        command = 'back ' + str(x)
        command = command.encode(encoding="utf-8") 
        self.log = self.client_socket.sendto(command, self.address)

    def move_up(self,x):
        command = 'up ' + str(x)
        command = command.encode(encoding="utf-8") 
        self.log = self.client_socket.sendto(command, self.address)
    
    def move_down(self,x):
        command = 'down ' + str(x)
        command = command.encode(encoding="utf-8") 
        self.log = self.client_socket.sendto(command, self.address)
    
    def move_left(self,x):
        command = 'left ' + str(x)
        command = command.encode(encoding="utf-8") 
        self.log = self.client_socket.sendto(command, self.address)

    def move_right(self,x):
        command = 'right ' + str(x)
        command = command.encode(encoding="utf-8") 
        self.log = self.client_socket.sendto(command, self.address)

    def rotate(self,x):
        command = 'cw ' + str(x)
        command = command.encode(encoding="utf-8") 
        self.log = self.client_socket.sendto(command, self.address)

    def get_life(self):
        command = 'battery?'
        command = command.encode(encoding="utf-8") 
        self.log = self.client_socket.sendto(command, self.address)

    def start_video_stream(self):
          command = 'streamon'
          command = command.encode(encoding="utf-8") 
          self.log = self.client_socket.sendto(command, self.address)


    def run_test(self):
        while True: 
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
       

