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
    input = 'hii'
        # Python 3 users
        # input = input(">> ")
    print "tx"
    ser.write(input + '\r\n')

def receive():
    out = ''
    out += ser.read(1)
    time.sleep(1)
    print "<<" + out


if __name__ == '__main__':

    # configure the serial connections (the parameters differs on the device you are connecting to)
   ser.isOpen()
   rospy.init_node('XBee_1', anonymous=true)
   pub=rospy.Publisher('XBee_1_TX', String, queue_size=10)
   rate=rospy.Rate(10)
   rospy.Subscriber("XBee_2_TX", String, receive)
   while not rospy.is_shutdown():
        hello_str = "hello %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()
