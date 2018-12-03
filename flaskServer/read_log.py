import time
from sendPacket import send_packet

def switch_in(address, switch_num):
    addressList = bytes.fromhex(address)

    # make data
    shifted_val = switch_num << 1
    packet_data = 1 + shifted_val
    print (address, packet_data, sep='<-')
    #send_packet(addressList, packet_data)

def switch_out(address, switch_num):
    addressList = bytes.fromhex(address)

    # make data
    shifted_val = switch_num << 1
    packet_data = 0 + shifted_val
    print(address, packet_data, sep='<-') # Print what is being sent where
    #send_packet(addressList, packet_data)

def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()

        # parse data
        if not line:
            time.sleep(0.1)
            continue
        elif(line[1:3] == 'B0' and int(line[4:6]) <= 100):
            print(line[1:3], line[4:6], line[7:9], line[10:12])
            if(line[7:9] == '10'):
                #switch thrown
                switch_out('0013A2004182F32D', int(line[4:6]))
                print('switch thrown\n')
            elif(line[7:9] == '30'):
                #switch closed
                switch_in('0013A2004182F32D', int(line[4:6]))
                print('switch closed\n')

if __name__ == '__main__':
    logfile = open("Py/MonitorLog.txt", "r")
    loglines = follow(logfile)
    for line in loglines:
        print (line)