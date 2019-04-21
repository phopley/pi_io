#!/usr/bin/env python
# Copyright 2019 Philip Hopley
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not 
# use this file except in compliance with the License. You may obtain a  copy
# of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#
# ROS node to read from and write to the Raspberry Pi GPIO
# Uses a ROS service to write outout to GPIO and used a Topic message when a monitored GPIO goes high
import sys
import rospy
import RPi.GPIO as GPIO
from pi_io.srv import gpio_output
from pi_io.msg import gpio_input

class PiGpioNode:
    def __init__(self):
        self.__output0 = 23       # GPIO Pin 23 is output index 0
        self.__output1 = 24       # GPIO Pin 23 is output index 1
        self.__input0 = 22        # GPIO Pin 22 is input index 0
        self.__input1 = 27        # GPIO Pin 27 is input index 1
        
        GPIO.setmode(GPIO.BCM)    # Use GPIO pin number not the physical pin numbering
        
        GPIO.setup(self.__output0, GPIO.OUT)
        GPIO.setup(self.__output1, GPIO.OUT)
        GPIO.setup(self.__input0, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.__input1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
        # Currently we only publish message when input goes high
        GPIO.add_event_detect(self.__input0, GPIO.RISING, callback=self.Input0HighCallback)
        GPIO.add_event_detect(self.__input1, GPIO.RISING, callback=self.Input1HighCallback)
        
        self.__service = rospy.Service('gpio/output_cmd', gpio_output, self.OutputCommand)        
        self.__gpi_pub = rospy.Publisher('gpio/input_cmd', gpio_input, queue_size=3)
        
    def OutputCommand(request):
        if(request.index == 0):
            gpo = self.__output0
        elif(request.index == 1):
            gpo = self.__output1
            
        GPIO.output(gpo, request.value)
      
    def Input0HighCallback(channel):
        input_cmd = gpio_input()
        input_cmd.index = 0
        input_cmd.value = True
        self.__gpi_pub.publish(input_cmd)

    def Input1HighCallback(channel):
        input_cmd = gpio_input()
        input_cmd.index = 1
        input_cmd.value = True
        self.__gpi_pub.publish(input_cmd)            
    

def main(args):
    rospy.init_node('pi_io_node', anonymous=False)
    rospy.loginfo("Rapberry Pi GPIO node started")    
    piio = PiGpioNode()

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print('Shutting down')

if __name__ == '__main__':
    main(sys.argv)


