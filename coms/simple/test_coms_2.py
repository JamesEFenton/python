import serial
import time

port = "COM9"
baud = 9600
parity = serial.PARITY_ODD
stopbits = serial.STOPBITS_ONE
bytesize = serial.SEVENBITS
#bytesize = serial.EIGHTBITS


##try: 
###    ser = serial.Serial(port, baud, serial.PARITY_NONE, bytesize, timeout=1)
#ser = serial.Serial(port, baud, timeout=1)
##    # open the serial port
##except:
##    print('Can''t open com port')
##    raw_input("Press Enter to exit")
##    exit()
    
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
