import socket
import sys
import struct, time
import math
from time import sleep
import os 

#IPADDR = str(sys.argv[1])
#IPADDR = '192.168.1.25'		#local network
#IPADDR = 'localhost'
#IPADDR = '92.25.34.80'		#home
IPADDR = 'ntp1.leontp.com'	#upu
PORTNUM = 123

PACKETDATA = bytearray(8)
#RX_PACKET  = bytearray(48)

# SOCK_DGRAM specifies that this is UDP
#s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
#s.connect((IPADDR, PORTNUM))
      
VERSION = 4
MODE = 7	#client

PACKETDATA[0] = VERSION << 3 | MODE
PACKETDATA[1] = 0		# seq
PACKETDATA[2] = 0x10	# implementation == 0x10
PACKETDATA[3] = 1		# req code

PACKETDATA[4] = 0
PACKETDATA[5] = 0
PACKETDATA[6] = 0
PACKETDATA[7] = 0

# reference time (in seconds since 1900-01-01 00:00:00)
TIME1970 = 2208988800L # 1970-01-01 00:00:00

# Create a UDP socket
server_address = (IPADDR, 123)

last_hits=0
last_ts1 = 0
last_ts0 = 0

while True:

 sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 sock.settimeout(2.5)

 newtime = int(time.time()) + 1
 while int(time.time()) < newtime:
   time.sleep(0.001)

 try:

    # Send data
    sent = sock.sendto(PACKETDATA, server_address)

    # Receive response
    RX_PACKET, server = sock.recvfrom(1024)

    ref_ts0 	= struct.unpack('<I',RX_PACKET[16:20])[0]
    ref_ts1 	= struct.unpack('<I',RX_PACKET[20:24])[0]
    NTP_served 	= struct.unpack('<I',RX_PACKET[28:32])[0]

    avg_hits = int((NTP_served - last_hits) / ((ref_ts1 - last_ts1) + (ref_ts0 - last_ts0) / 4294967296.0 ) + 0.5)

    if (avg_hits > 0) and ((ref_ts1 - last_ts1) < 120):
		callargs = "rrdtool update ntp1.rrd " + str(last_ts1 - TIME1970) + ":" + str(avg_hits)  # timestamp is beginning of interval 
		os.system(callargs)

    last_hits = NTP_served
    last_ts1 = ref_ts1
    last_ts0 = ref_ts0

 finally:
    sock.close()
