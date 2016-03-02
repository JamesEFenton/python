import serial
import time


# these are allowed
# ser = serial.Serial("COM9", 9600, bytesize=8, parity='N', stopbits=1,timeout=1, xonxoff=0, rtscts=0)
# ser = serial.Serial("COM9", 9600, bytesize=7, parity='N', stopbits=1,timeout=1, xonxoff=0, rtscts=0)
# ser = serial.Serial("COM9", 9600, bytesize=7, parity='O', stopbits=1,timeout=1, xonxoff=0, rtscts=0)

try:
    ser = serial.Serial("COM9", 19200, bytesize=7, parity='O', stopbits=1, timeout=0, xonxoff=0, rtscts=0)
    # open the serial port
except:
    print('Can''t open com port')
    raw_input("Press Enter to exit")
    exit()

test_message = "1234567890\n"    
if ser.isOpen():
    print(ser.name + ' is open...')
    print('Try and write the following 10 chars:' + test_message)
    ser.write(test_message)
    time.sleep(1)
    #read_message = ser.read(10)
    read_message = ""
    while ser.inWaiting() > 0:
        read_message += ser.read(1)
    print('Read the following back:' + read_message)
    
ser.close()


        

