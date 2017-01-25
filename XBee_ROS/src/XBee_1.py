#!/usr/bin/env python
import time
import serial
import rospy
import thread
from std_msgs.msg import String


ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
    )

def send():
    input = 'hii'
        # Python 3 users
        # input = input(">> ")
    rospy.loginfo("Txed The signal")
    pub_tx.publish(input)
    ser.write(input + '\r\n')

def receive():
    out = ''
    out += ser.read(10)
    time.sleep(1)
    pub_rx.publish(out)
    rospy.loginfo("Rcvd Mssg"+out)


if __name__ == '__main__':

    # configure the serial connections (the parameters differs on the device you are connecting to)
    ser.isOpen()
    rospy.init_node('XBee_1')
    pub_tx=rospy.Publisher('XBee_1_TX', String, queue_size=10)
    pub_rx=rospy.Publisher('XBee_1_RX', String, queue_size=10)
    rate=rospy.Rate(0.1)
    thread.start_new_thread(receive,())
    while not rospy.is_shutdown():
        thread.start_new_thread(send,())        
        rate.sleep()    