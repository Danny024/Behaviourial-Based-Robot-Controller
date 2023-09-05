# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 20:59:28 2022

@author: Eneh Daniel Anietie
"""

from controller import Robot
from datetime import datetime
import math
import sys
import os
import time

class Controller :
   
    
    def __init__(self,robot):
        self.robot = robot
        self.timestep = int(robot.getBasicTimeStep())
        self.max_speed = 6.28 #ms
        
        #Let the robot assume initially that they are no black maze
        self.black_maze = False
        
        #Enable motors
        self.left_motor = self.robot.getDevice('left wheel motor')
        self.right_motor = self.robot.getDevice ('right wheel motor')
        self.left_motor.setVelocity(0.0)
        self.right_motor.setVelocity(0.0)
        self.left_motor.setPosition(float('inf'))
        self.right_motor.setPosition(float ('inf'))
        self.left_speed = 0
        self.right_speed = 0
        
        #Enable proximity sensors
        self.prox_sensors = []
        for ind in range (8):
            sensor_name = 'ps' + str(ind)
            self.prox_sensors.append(self.robot.getDevice(sensor_name))
            self.prox_sensors[ind].enable(self.timestep)
        
        #Enable Ground Sensors   
        
        self.left_ir = self.robot.getDevice('gs0')
        self.left_ir.enable(self.timestep)
        self.center_ir = self.robot.getDevice('gs1')
        self.center_ir.enable(self.timestep)
        self.right_ir = self.robot.getDevice('gs2')
        self.right_ir.enable(self.timestep)
        
        
    #Function to check if a black square box has been detected
    #If the ground sensor reading is less than 500 it is black otherwise it is a white
    def maze_check (self):
        if (self.center_ir.getValue() < 500): #If ground sensor get a value less than 500 a black maze is spotted
            self.black_maze = True
            print ('black maze identified')
            
        
    #Function to turn robot full right (ie 90 degrees to the right)     
    def turn_right (self):
        self.left_speed = self.max_speed/2
        self.right_speed = -self.max_speed/2
        print ('driving right')
      
    #Function to turn robot full left (ie 90 degrees to the left)      
    def turn_left(self):
        self.left_speed = -self.max_speed
        self.right_speed = self.max_speed
        print ('driving left')
        
    #Function to drive the robot forward 
    def drive_forward(self):
        if (self.left_corner_reading > self.right_corner_reading):
            self.tilt_right ()
        elif (self.right_corner_reading > self.left_corner_reading):
            self.tilt_left ()
        if (self.right_corner_reading == self.left_corner_reading):
            self.left_speed = self.max_speed/2
            self.right_speed = self.max_speed/2
        print ('driving forward')
         
             
     # Function to stop the robot when it arrives its destination   
    def stop(self):
        self.left_speed = 0.0
        self.right_speed = 0.0
        print(" ")
        print ("Obstacle Detected")
        print("")
        print ("Destination Reached")
        print(" ")
        print ("*********  Instruction Manual To Rerun Simulation  ******")
        print ("1. Pause the Simulation")
        print ("2. Reset Robot position to origin (ie Start position)")
        print ("3. Then Reload World to rerun the simulation")   
        
        
    #Function to tilt the robot right   
    def tilt_right (self):
        self.left_speed = self.max_speed/2.0
        self.right_speed = self.max_speed / 4.0
        print ('tilting  right')
        
    #Function to tilt the robot left 
    def tilt_left (self):
        self.left_speed = self.max_speed/4.0
        self.right_speed = self.max_speed/2.0
        print ('tilting left')
        
        
        
    def run_robot(self):
        
        #Main loop
        #- perform simulation step until Webot is stopping the controller
        while self.robot.step(self.timestep) != -1:
             #Read the sensors:
            min_gs = 0   #minimum value for ground sensors
            max_gs = 1000 #maximum value for ground sensors
            self.ground_sensors = []   
            left = self.left_ir.getValue()
            center = self.center_ir.getValue()
            right = self.right_ir.getValue()
            if (left > max_gs) : left = max_gs
            if (center > max_gs) : center = max_gs
            if (right > max_gs) : right = max_gs
            if (left < min_gs) : left = min_gs
            if (center < min_gs) : center = min_gs
            if (right < min_gs) : right = min_gs
            self.ground_sensors.append(left)
            self.ground_sensors.append(center)
            self.ground_sensors.append(right)
            print("Ground Sensors \n    left {} center {} right {}".format(self.ground_sensors[0],self.ground_sensors[1],self.ground_sensors[2]))
            #Check for black_count
            
                
            for i in range(8):
                if(i==0 or i==1 or i==2 or i==5 or i==6 or i==7):  
                    # Adjust Values
                  
                    print("Distance Sensors - Index: {}  Value: {}".format(i,self.prox_sensors[i].getValue()))        
            
            #Note : The bigger the proximity sensor value the closer it is to an obstacle
            #Note ps stands for Proxmity sensor
            self.right_wall = self.prox_sensors[2].getValue()>80 #Detects if there is a right wall using sensor ps2 and returns True or False
            self.left_wall = self.prox_sensors[5].getValue()>80 #Detects if there is a left wall using sensor ps5 and returns True or False
            self.front_wall = (self.prox_sensors[7].getValue() + self.prox_sensors[0].getValue())/2>80 #Detects if there is a front wall by using the avrerage of ps0 and ps7 sensors 
            self.left_corner_reading = self.prox_sensors[6].getValue() #Detects the reading for left corner using ps6 sensor
            self.right_corner_reading = self.prox_sensors[1].getValue() #Detects the reading for right corner using ps1 sensor
            self.left_corner = self.left_corner_reading > 80 #Detects if there is a wall at the left_corner
            self.right_corner = self.right_corner_reading > 80 #Detects if there is a wall at the right_corner
            print ('The left wall status is : ', self.left_wall)
            print ('The right wall status is : ',self.right_wall)
            print ('The front wall status is : ',self.front_wall)
            
            #Check for black_square on maze
            self.maze_check()
            print ('The black maze status is :', self.black_maze)
            
            
            if (self.front_wall == True): #If there is a front wall
              
                
                if ((self.left_wall== False) and (self.black_maze == True)): #if there is no left wall and black_square has been detected
                    self.turn_right() 
                elif ((self.right_wall==False) and (self.black_maze == False)): #if there is no right wall and  black square has not been detected
                    self.turn_left()
                elif (self.right_corner and self.left_corner): #if there is a right_corner and left_corner 
                    self.stop()
            else :
                self.drive_forward()
                
            #sends actuator commands to motor:
            self.left_motor.setVelocity(self.left_speed)
            self.right_motor.setVelocity(self.right_speed)
            
           
    
        
        
if __name__ == "__main__":
    my_robot = Robot()
    controller = Controller(my_robot)
    controller.run_robot() 
           