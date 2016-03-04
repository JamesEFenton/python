import Tkinter, tkFileDialog
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
    elif(-1!=cmd[0].find("read")):
        command1 = "r"
        debug_print("Let's read")
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

def select_log_directory():
    test_dir = "C:\\Git\\GitHub\\python\\coms\\simple"
    # Choose an output folder
    root = Tkinter.Tk()
    root.withdraw()
    out_folder = tkFileDialog.askdirectory(initialdir=test_dir)
    return out_folder

def select_test_command_file():
    test_dir = "C:\\Git\\GitHub\\python\\coms\\simple"
    # Get file
    root = Tkinter.Tk()
    root.withdraw()
    test_file = tkFileDialog.askopenfilename(initialdir=test_dir, filetypes=[("Test file","*.txt")])
    return test_file

def write_log_file_header(logfile, test_file, log_filename):
    logfile.write("Freya comms log created: " + time.asctime() + "\n\n")
    logfile.write("Test file executed: " + test_file + "\n\n")
    logfile.write("Log file recorded: " + log_filename + "\n\n")    
   
if __name__ == '__main__':
    global debug
    global baud_rate
    # this works baud_rate = 115200
    #baud_rate = 9600 # tout = 0.1 File transfer took: 75.853000164 seconds
    #baud_rate = 115200 # tout = 0.1 File transfer took: 32.7369999886 seconds
    #baud_rate = 230400 # tout = 0.1 File transfer took: 30.875 seconds
    # this works but slow    baud_rate = 921600
    baud_rate = 115200
    #debug = True
    debug = False
    file_running = False
    sleep_time = 0
    tout = 0.1
    try:
        # open the serial port
        ser = serial.Serial(port_id, baud_rate, bytesize=7, parity='O', stopbits=1, timeout=tout, xonxoff=0, rtscts=0)
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
        if(file_running != False):
            #get another line test_file
            if(test_file!=""):
                start = time.time()
                try:
                                    # Write to output file
                    results_file = log_directory + "\\comms_log.csv"
                    logfile = open(results_file, 'w+')
                    write_log_file_header(logfile, test_file, results_file)
                except:
                    print("Can't open log file: " + results_file)
                        
                with open(test_file) as infile:
                    found_input = False
                    for line in infile:
                        timestamp = time.strftime('%X')
                        out = (timestamp + "," + line)
                        print(out)
                        logfile.write(out)
                        output_cmd = build_message(line)
                        ser.flushInput()
                        ser.write(output_cmd.encode('ascii')+'\r\n')
                        time.sleep(sleep_time)
                        out = ser.readline()
                        print('Received,'+out)
                        out = (timestamp + "," + out)
                        logfile.write(out)
                logfile.close()
                # Test file has been sent so clear flag
                file_running = False
                done = time.time()
                elapsed = done - start
                print("File transfer took: " + str(elapsed) + " seconds")
            else:
                file_running = False
        else:
            cmd = raw_input("Enter command or 'file' or 'exit':")
            
        if(cmd == 'file'):
            file_running = True
            test_file = select_test_command_file()
            if (test_file!=""):
                log_directory = select_log_directory()
            cmd = ""
        elif(cmd == 'exit'):
            ser.close()
        elif(cmd != ''):
            output_cmd = build_message(cmd)
            ser.flushInput()
            ser.write(output_cmd.encode('ascii')+'\r\n')
            time.sleep(sleep_time)
            out = ser.readline()
            print('Received...'+out)
