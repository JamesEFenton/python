import serial
import time

port_id = "COM9"

def debug_print(message):
    global debug
    if (debug != False):
        print(message)
    
def build_message(command):
    message = ""
    #split up the message
    cmd = command.split()
    debug_print("Split found: " + str(len(cmd)))
    if(len(cmd) == 0):
        print("No command")
        command = ""
    elif(-1!=cmd[0].find("write")):
        command1 = "w"
        debug_print("Let's write")
        #key = command[6:13]
        #value = command[14:17]
    elif(-1!=cmd[0].find("read")):
        command1 = "r"
        debug_print("Let's read")
        #key = command[5:12]
    else:
        print("I don't understand your read/write command")
        command1 = ""
        command = ""
    if(command!=""):
        choices = {'motor_1': '0001', 'motor_2': '0002', 'motor_3': '0003', 'adc_1': '0010', 'adc_2': '0011'}
        result = choices.get(cmd[1], 'not_found')
        if(result != 'not_found'):
            debug_print("to : " + cmd[1])
            message = command1 + result
        else:
            print("I don't understand your device: " + cmd[1])
            command = ""
    if(len(cmd) > 2): # long command - probably has a value
        debug_print("this value: " + cmd[2])
        try:
            val = int(cmd[2])
            message = message + cmd[2]
        except:
            print("This is not a good value")
    return message

if __name__ == '__main__':
    global debug
    #debug = True
    debug = False
    try:
        # open the serial port
        ser = serial.Serial(port_id, 9600, bytesize=7, parity='O', stopbits=1, timeout=1, xonxoff=0, rtscts=0)
    except:
        print('Can''t open ' + port_id + ' port')
        raw_input("Press Enter to exit")
        exit()
        
    if ser.isOpen():
         print(ser.name + ' is open...')
         #ser.write("Hello from the PC side")
         
     
    while ser.isOpen():
        out = ser.read()
        print(out)       
        cmd = raw_input("Enter command or 'exit':")
        if cmd == 'exit':
            ser.close()
        else:
            output_cmd = build_message(cmd)
            ser.flushInput()
            ser.write(output_cmd.encode('ascii')+'\r\n')
            time.sleep(1)
            out = ser.readline()
            print('Received...'+out)
