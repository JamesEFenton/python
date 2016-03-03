import serial
import time

port_id = "COM10"

def decode_message(message):
    global comm_count
    global bad_comm_count    
    device = ""
    value = 0
    if(message[0] == "w"):
        write = True
        read = False
        write_access = True
        debug_print("Let's write to ")
    elif(message[0] == "r"):
        write = False
        read = True
        write_access = False
        debug_print("Let's read from ")
    else:
        write = False
        read = False
        write_access = False
        print("I don't understand your read/write command")
        #shouldn't get here
        bad_comm_count = bad_comm_count + 1

    if(len(message) > 4):
        key = message[1:5]
        choices = {'0001':'motor_1', '0002':'motor_2', '0003':'motor_3', '0010':'adc_1', '0011':'adc_2'}
        device = choices.get(key, 'not_found')
        if(device != 'not_found'):
            debug_print("device : " + device)
            if(len(message) > 8):
                value = int(message[5:9])
            else:
                value = 0
        else:
            print("I don't understand your device: " + key)
            device = ""
            #shouldn't get here
            bad_comm_count = bad_comm_count + 1
    return write_access, device, value

def simulate_cpld(access, dev, val):
    global comm_count
    global bad_comm_count
    value = ""
    if(-1!=dev.find("motor")):
        value = drive_motor(access, dev, val)
    elif(-1!=dev.find("adc")):
        value = drive_adc(access, dev, val)
    else:
        #shouldn't get here
        bad_comm_count = bad_comm_count + 1
        value = "4242"
    return value

def drive_motor(access, dev, val):
    value = "0000"
    return value

def drive_adc(access, dev, val):
    global adc_value1
    global adc_value2    
    if(-1!=dev.find("adc_1")):
        value = adc_value1 = adc_value1 + 1
    else:
        value = adc_value2 = adc_value2 + 1
    return str(value)

def debug_print(message):
    global debug
    if (debug != False):
        print(message)
        
if __name__ == '__main__':
    global adc_value1
    global adc_value2
    global debug
    global comm_count
    global bad_comm_count
    global baud_rate
    # this works baud_rate = 115200
    #baud_rate = 9600 # File transfer took: 75.853000164 seconds
    #baud_rate = 115200 #File transfer took: 32.7369999886 seconds
    #baud_rate = 230400
    baud_rate = 115200
    # this works but slow    baud_rate = 921600 
    comm_count = 0
    bad_comm_count = 0
    adc_value1 = 0
    adc_value2 = 0
    #debug = True
    debug = False
    tout = 0.1
    try:
        # open the serial port
        ser = serial.Serial(port_id, baud_rate, bytesize=7, parity='O', stopbits=1, timeout=tout, xonxoff=0, rtscts=0)
    except:
        print('Can''t open com port')
        raw_input("Press Enter to exit")
        exit()
        
    if ser.isOpen():
         print(ser.name + ' is open...')
         print('Receiving...')
     
    while True:
        command = ""
        command = ser.readline()
        #print("." + command)
        #echo it back
        output_message = command
        if(len(output_message) > 0):
            comm_count = comm_count + 1
            print("command recieved: " + command)
            access, dev, val = decode_message(command)
            debug_print("decoded device: " + dev)
            debug_print("decoded value: " + str(val))
            output_message = simulate_cpld(access, dev, val)
            debug_print("Sending back:" + output_message)
            ser.write(output_message.encode('ascii')+'\r\n')

            

