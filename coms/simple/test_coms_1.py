import serial
import time


# these are allowed
# ser = serial.Serial("COM9", 9600, bytesize=8, parity='N', stopbits=1,timeout=1, xonxoff=0, rtscts=0)
# ser = serial.Serial("COM9", 9600, bytesize=7, parity='N', stopbits=1,timeout=1, xonxoff=0, rtscts=0)
# ser = serial.Serial("COM9", 9600, bytesize=7, parity='O', stopbits=1,timeout=1, xonxoff=0, rtscts=0)

try:
    ser = serial.Serial("COM9", 9600, bytesize=7, parity='O', stopbits=1, timeout=1, xonxoff=0, rtscts=0)
    # open the serial port
except:
    print('Can''t open com port')
    raw_input("Press Enter to exit")
    exit()
    
if ser.isOpen():
     print(ser.name + ' is open...')
     print('Receiving...')
 
while True:
    #time.sleep(2)
    out = ser.read()
    print(out)

        
##    cmd = raw_input("Enter command or 'exit':")
##        # for Python 2
##    # cmd = input("Enter command or 'exit':")
##        # for Python 3
##    if cmd == 'exit':
##        ser.close()
##        exit()
##    else:
##        ser.write(cmd.encode('ascii')+'\r\n')
##        out = ser.read()
##        print('Receiving...'+out)
