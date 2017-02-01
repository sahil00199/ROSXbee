#!/usr/bin/env python

import time
import serial
import rospy
import thread
from std_msgs.msg import String
from collections import deque
from sensor_msgs.msg import NavSatFix

class gps_data:
    latitude = "0.0"
    longitude = "0.0"
    altitude = "0.0"

    def __int__():
        latitude = "0.0"
        longitude = "0.0"
        altitude = "0.0"
    
    def callback(self , data):
        #rospy.loginfo("lat is: " + str(data.latitude))
        #rospy.loginfo("long is: " + str(data.longitude))
        #rospy.loginfo("alt is: " + str(data.altitude))
        self.latitude = str(data.latitude)
        self.longitude = str(data.longitude)
        self.altitude = str(data.altitude)

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS,
    timeout = 1
    )



def send():
    backlog = deque('')
    input = gps_data()
    rospy.Subscriber("/mavros/global_position/raw/fix", NavSatFix, input.callback)
    #rospy.loginfo(input.latitude)
        # Python 3 users
        # input = input(">> ")
    backlog.extendleft("start/")
    backlog.extendleft(input.latitude + "/")
    backlog.extendleft(input.longitude + "/")
    backlog.extendleft(input.altitude)
    backlog.extendleft("/stop")
    while not len(backlog) == 0:
        x = backlog.pop()
        pub_tx.publish(x)
        rospy.loginfo("sent: " + x)
        ser.write(x + '\r\n')
        #rospy.loginfo("txed")

def receive():
    backlog = deque('')
    out = ser.read(10)
    #rospy.loginfo(out)
    backlog.extendleft(out)
    #time.sleep(1)
    #while 1:
     #  rospy.loginfo(backlog)
    #   time.sleep(1)
    dis = ''
    while not len(backlog) == 0:
        dis += backlog.pop()
    if dis != '':
        pub_rx.publish(dis)
        rospy.loginfo(dis)


if __name__ == '__main__':

    # configure the serial connections (the parameters differs on the device you are connecting to)
    ser.isOpen()
    rospy.init_node('XBee_1')
    pub_tx=rospy.Publisher('XBee_1_TX', String, queue_size=10)
    pub_rx=rospy.Publisher('XBee_1_RX', String, queue_size=10)
    rate=rospy.Rate(1)
    thread.start_new_thread(receive,())
    while not rospy.is_shutdown():
        thread.start_new_thread(send,())
        thread.start_new_thread(receive, ())        
        rate.sleep()    