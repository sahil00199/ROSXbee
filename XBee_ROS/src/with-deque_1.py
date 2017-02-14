#!/usr/bin/env python

import time
import serial
import rospy
import thread
from std_msgs.msg import String
from collections import deque
from sensor_msgs.msg import NavSatFix

ser = serial.Serial(
    port='/dev/ttyUSB1',
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS,
    timeout = 1
    )


class gps_data:
    latitude = "0.0"
    longitude = "0.0"
    altitude = "0.0"

    def __int__():
        latitude = "0.0"
        longitude = "0.0"
        altitude = "0.0"

def callback(data):
    #input = gps_data()
    #input.latitude = str(data.latitude)
    #input.longitude = str(data.longitude)
    #input.altitude = str(data.altitude)
    backlog = deque('')
    backlog.extendleft("@")
    backlog.extendleft(str(data.latitude) + "/")
    backlog.extendleft(str(data.longitude) + "/")
    backlog.extendleft(str(data.altitude))
    backlog.extendleft("$")
    backlog.extendleft("\n")
    while not len(backlog) == 0:
        x = backlog.pop()
        pub_tx.publish(x)
        rospy.loginfo("sent: " + x)
        ser.write(x)
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
    rospy.Subscriber("/mavros/global_position/raw/fix", NavSatFix, callback)
    while not rospy.is_shutdown():
        thread.start_new_thread(receive, ())        
        rate.sleep()    
