#!/usr/bin/env python

import time
import serial
import rospy
import thread
from std_msgs.msg import String
from collections import deque
from sensor_msgs.msg import NavSatFix

class gps_data:
    latitude = ""
    longitude = ""
    altitude = ""

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
    input = ''
    
    while not len(backlog) == 0:
        x = backlog.pop()
        pub_tx.publish(x)
        rospy.loginfo("sent: " + x)
        ser.write(x + '\r\n')
        #rospy.loginfo("txed")

def receive():
    message = deque('')
    out = ser.read(10)
    message.extendleft(out)
    mes = ''
    while not len(message) == 0:
        mes += message.pop()
    if len(mes) != 0:
        dis = mes.split('@' , 1)[1]
        dis = dis.split('$' , 1)[0]
        mes = mes.split('$' , 1)[1]
        if dis != '':
            pub_rx.publish(dis)
            rospy.loginfo(dis)


if __name__ == '__main__':

    # configure the serial connections (the parameters differs on the device you are connecting to)
    ser.isOpen()
    rospy.init_node('XBee_1')
    pub_tx=rospy.Publisher('XBee_1_TX', String, queue_size=10)
    pub_rx=rospy.Publisher('XBee_1_RX', String, queue_size=10)
    rate=rospy.Rate(2)
    thread.start_new_thread(receive,())
    while not rospy.is_shutdown():
        thread.start_new_thread(send,())
        thread.start_new_thread(receive, ())        
        rate.sleep()    
