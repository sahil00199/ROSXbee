#!/usr/bin/env python

import time
import serial
import rospy
from std_msgs.msg import String
from multiprocessing import Process

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
    )

def send():
    hello_str = "hello %s" % rospy.get_time()
    pub.publish(hello_str)
        
        # Python 3 users
        # input = input(">> ")
    #rospy.loginfo("tx")
    #ser.write(hello_str)

def receive():
    out = ''
    out += ser.read(1)
    time.sleep(1)
    rospy.loginfo(out) 


if __name__ == '__main__':

    # configure the serial connections (the parameters differs on the device you are connecting to)
   ser.isOpen()
   rospy.init_node('XBee_2')
   pub=rospy.Publisher('XBee_2_TX', String, queue_size=10)
   rate=rospy.Rate(10)
   rospy.Subscriber("XBee_1_TX", String, receive)
   while not rospy.is_shutdown():
        send()
        rate.sleep()