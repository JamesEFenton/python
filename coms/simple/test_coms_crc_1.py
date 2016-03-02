import serial
import time
import minimalmodbus

# these are allowed
# ser = serial.Serial("COM9", 9600, bytesize=8, parity='N', stopbits=1,timeout=1, xonxoff=0, rtscts=0)
# ser = serial.Serial("COM9", 9600, bytesize=7, parity='N', stopbits=1,timeout=1, xonxoff=0, rtscts=0)
# ser = serial.Serial("COM9", 9600, bytesize=7, parity='O', stopbits=1,timeout=1, xonxoff=0, rtscts=0)
# ser = serial.Serial("COM9", 19200, bytesize=8, parity='E', stopbits=1, timeout=0, xonxoff=0, rtscts=0)

try:
    ser = serial.Serial("COM9", 19200, bytesize=8, parity='N', stopbits=1, timeout=0, xonxoff=0, rtscts=0)
    # open the serial port
except:
    print('Can''t open com port')
    raw_input("Press Enter to exit")
    exit()

test_message = "123456789012345"    
##if ser.isOpen():
##    print(ser.name + ' is open...')
##    print('Try and write the following ' + str(len(test_message)) + ' chars:' + test_message)
##    ser.write(test_message)
##    time.sleep(1)
##    read_message = ""
##    while ser.inWaiting() > 0:
##        read_message += ser.read(1)
##    print('Read the following ' + str(len(read_message)) + ' characters back:' + read_message)
##    time.sleep(1)
##    test_message = "abcdefghijklmno"
##    print('Try and write the following ' + str(len(test_message)) + ' chars:' + test_message)
##    ser.write(test_message)
##    time.sleep(1)
##    #read_message = ser.read(10)
##    read_message = ""
##    while ser.inWaiting() > 0:
##        read_message += ser.read(1)
##    print('Read the following ' + str(len(read_message)) + ' characters back:' + read_message)    
ser.close()

time.sleep(2)
try:
    instrument = minimalmodbus.Instrument('COM9', 1)
    instrument.debug = True
    instrument.mode = minimalmodbus.MODE_RTU
    #instrument.mode = minimalmodbus.MODE_ASCII
    print("minimalmodbus.BAUDRATE" + str(minimalmodbus.BAUDRATE))
    print("minimalmodbus.PARITY" + (minimalmodbus.PARITY))
    print("minimalmodbus.BYTESIZE" + str(minimalmodbus.BYTESIZE))
    print("minimalmodbus.STOPBITS" + str(minimalmodbus.STOPBITS))
    print("minimalmodbus.TIMEOUT" + str(minimalmodbus.TIMEOUT))
    print("minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL" + str(minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL))
    print("minimalmodbus.BAUDRATE" + str(minimalmodbus.BAUDRATE))


except:
    print("Can't create instrument")

try:
    temperature = instrument.read_register(289, 1)
except:
    print("Can't read instrument")

        
# if I set bytesize=8
# must set UartHandle.Init.WordLength   = UART_WORDLENGTH_9B; on ST
