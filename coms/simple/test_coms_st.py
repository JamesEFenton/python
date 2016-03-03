import serial
import time

port_id = "COM10"

def build_message(command):
    if(-1!=command.find("write")):
        command1 = "w"
        debug_print("Let's write")
        key = command[6:13]
    elif(-1!=command.find("read")):
        command1 = "r"
        debug_print("Let's read")
        key = command[5:12]
    else:
        print("I don't understand your read/write command")
        command1 = ""
        command = ""
    if(command!=""):
        choices = {'motor_1': 1, 'motor_2': 2, 'motor_3': 3, 'adc_1': 10, 'adc_2': 11}
        result = choices.get(key, 'not_found')
        if(result != 'not_found'):
            debug_print("to : " + key)
            command = command1 + str(result)
        else:
            print("I don't understand your device: " + key)
            command = ""
    return command

def decode_message(message):
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
    return write_access, device, value

def simulate_cpld(access, dev, val):
    value = ""
    if(-1!=dev.find("motor")):
        value = drive_motor(access, dev, val)
    elif(-1!=dev.find("adc")):
        value = drive_adc(access, dev, val)
    else:
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
    
    adc_value1 = 0
    adc_value2 = 0
    #debug = True
    debug = False
    try:
        # open the serial port
        ser = serial.Serial(port_id, 9600, bytesize=7, parity='O', stopbits=1, timeout=1, xonxoff=0, rtscts=0)
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
            print("command recieved: " + command)
            access, dev, val = decode_message(command)
            debug_print("decoded device: " + dev)
            debug_print("decoded value: " + str(val))
            output_message = simulate_cpld(access, dev, val)
            debug_print("Sending back:" + output_message)
            ser.write(output_message.encode('ascii')+'\r\n')
            #ser.write(command)
            

