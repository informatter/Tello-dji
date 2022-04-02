
from dis import Instruction
import threading 
import socket
import time
import logging
from tello_constants import*


class Tello:

    def __init__(self, client_machine_ip: str = ''):
       
        # self.port = 9000
        self.address = (TELLO_IP_ADRESS, TELLO_PORT_NUM)
        self.client_machine = (client_machine_ip,TELLO_PORT_NUM) #(self.client_machine_ip,self.port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.log =''
        self.can_run = True
        self.counter = 0
        self.last_command_received_at = time.time()
        self.tello_responses =[]
        self.receive_response_thread = threading.Thread(target = self.__receive_response_from_tello)
        self.receive_response_thread.daemon = True
        self.receive_response_thread.start()
        self.client_socket.bind(self.client_machine)

    def __receive_response_from_tello(self):
        while True: 
            try:
                data, address = self.client_socket.recvfrom(1518)
                address = address[0]
                print('Data received from {} at client_socket'.format(address))
                if(address!=self.address[0]): continue
                striped_data = data.rstrip("\r\n")
                self.tello_responses.append(striped_data)
            except Exception:
                print ("An error occured while receiving a response from Trello ):")
                break

    def __try_send_control_command(self, command:str) -> str:

        delta_time = time.time() - self.last_command_received_at

        # gives a waiting threshold of the next command
        # request if interval was to short.
        if delta_time < 0.5: time.sleep(delta_time)

        self.client_socket.sendto(command.encode('utf-8'), self.address)
        print("Sent {} to Trello".format(command))
        current_time = time.time()
       
        # If there are no responses, will check time out, if time
        # has exeeded, this method will abort.
        while not self.tello_responses:
            # aborts command if did not receive response back from Tello
            # after response timeout
            if time.time() - current_time > RESPONSE_TIMEOUT:
                error_message = "Aborting command '{}'. Did not receive a response after the timeout of {} seconds".format(command, RESPONSE_TIMEOUT)
                print( error_message)
                return error_message

            # sleeps main thread for a few ms 
            # if response timeout is not met
            time.sleep(0.1)

        self.last_command_received_at = time.time()
        # returns latest response.
        first_response = self.tello_responses.pop(0)
        try:
            response = first_response.decode("utf-8")
        except UnicodeDecodeError as e:
            error_message = "Encountered an error while decoding response:{}".format(e)
            return error_message

        # response = response.rstrip("\r\n")
        print("Response from command {}: '{}'".format(command, response))
        return response

    # Send a command which controls the behavior of Tello
    def send_action_command(self, command:str):
        
        response = "max retries exceeded"
        for i in range(0, MAX_RETRY_COMMAND_COUNT):
            response = self.__try_send_control_command(command)
            lower_case_response = response.lower()
            print("lower_case_response: {}".format(lower_case_response))
            if 'ok' in lower_case_response:
                print("Tello says: {} after completing {}".format(lower_case_response,command))
                return

            print("Command attempt #{} failed for command: '{}'".format(i, command))

        print("Max retries for command {} have exceeded".format(command))


    def connect(self):
         self.send_action_command('command')
        #  command ='command'
        #  command = command.encode(encoding="utf-8") 
        #  self.log = self.client_socket.sendto(command, self.address)

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
        command = 'right ' + str(x)
        self.send_action_command(command)

    # Moves the drone x cm's to the left.
    # "x" should be between 20 - 500 cm.
    def move_left(self,x):
        command = 'left ' + str(x)
        self.send_action_command(command)
    def flip_back(self):
        command = 'flip b'
        self.send_action_command(command)


     # Moves the drone x cm's forward.
     # "x" should be between 20 - 500 cm.
    def move_forward(self,x):
        command = 'forward ' + str(x)
        self.send_action_command(command)

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
        self.send_action_command(command)

    def move_right(self,x):
        command = 'right ' + str(x)
        command = command.encode(encoding="utf-8") 
        self.log = self.client_socket.sendto(command, self.address)

    def rotate(self,x):
        command = 'cw ' + str(x)
        self.send_action_command(command)

    def get_life(self):
        self.send_action_command('battery?')

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
       

