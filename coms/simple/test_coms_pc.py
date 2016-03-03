import serial
import time

port_id = "COM9"

def build_message(command):
    if(-1!=command.find("write")):
        command1 = "w"
        print("Let's write")
        key = command[6:13]
    elif(-1!=command.find("read")):
        command1 = "r"
        print("Let's read")
        key = command[5:12]
    else:
        print("I don't understand your read/write command")
        command1 = ""
        command = ""
    if(command!=""):
        choices = {'motor_1': 1, 'motor_2': 2, 'motor_3': 3, 'adc_1': 10, 'adc_2': 11}
        result = choices.get(key, 'not_found')
        if(result != 'not_found'):
            print("to : " + key)
            command = command1 + str(result)
        else:
            print("I don't understand your device: " + key)
            command = ""
    return command

if __name__ == '__main__':
    
    try:
        # open the serial port
        ser = serial.Serial(port_id, 9600, bytesize=7, parity='O', stopbits=1, timeout=1, xonxoff=0, rtscts=0)
    except:
        print('Can''t open ' + port_id + ' port')
        raw_input("Press Enter to exit")
        exit()
        
    if ser.isOpen():
         print(ser.name + ' is open...')
         ser.write("Hello from the PC side")
         
     
    while ser.isOpen():
        out = ser.read()
        print(out)       
        cmd = raw_input("Enter command or 'exit':")
        if cmd == 'exit':
            ser.close()
            #exit()
        else:
            output_cmd = build_message(cmd)
            ser.write(output_cmd.encode('ascii')+'\r\n')
            time.sleep(1)
            out = ser.read()
            print('Received...'+out)
