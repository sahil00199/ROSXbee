import time
import serial
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
    ser.write(input + '\r\n')

def receive():
    out = ''
    out += ser.read(1)
    time.sleep(1)
    print "<<" + out


if __name__ == '__main__':

    # configure the serial connections (the parameters differs on the device you are connecting to)
   

    ser.isOpen()

    p = Process(target=send, args=())
    q = Process(target=receive, args=())
    p.start()
    q.start()
    p.join()
    q.join()