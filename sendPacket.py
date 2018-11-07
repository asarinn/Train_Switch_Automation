import time
import serial

# Generate the packet to send
def frame_gen(address, data):
    #packet = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    packet = [None] * 19
    checksum = 0

    # Start delimiter
    packet[0] = 0x7E

    # Length
    packet[1] = 0x00
    packet[2] = 0x0F

    # Frame type
    packet[3] = 0x10

    # Frame ID
    packet[4] = 0x01

    # 64 bit address
    for x in range (5, 13):
        packet[x] = address[x-5]

    # 16 bit address
    packet[13] = 0xFF
    packet[14] = 0xFE

    # Broadcast radius
    packet[15] = 0x00

    # Options
    packet[16] = 0x00

    # Data
    packet[17] = data

    # Checksum
    for x in range (3, 18):
        checksum += packet[x]
    checksum = checksum & 0xFF
    packet[18] = 0xFF - checksum

    return packet

address = [0x00,0x13,0xA2,0x00,0x41,0x82,0xF3,0x2D]
packet = frame_gen(address, 0x01)
for x in range(0, 19):
    print("%5X"% (packet[x]))

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

while 1:
    ser.write(packet)
    time.sleep(1)
