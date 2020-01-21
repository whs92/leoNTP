#run as python LeoNTP-stats-full.py SERVER_NAME
#display current statistics of the LeoNTP server using private mode 7 request

import socket
import sys
import struct, time
import math
import binascii
from time import sleep

#IPADDR = 'ntp1.leontp.com'
IPADDR = str(sys.argv[1])	# the only cmd line argument is NTP server address
PORTNUM = 123
VERSION = 4	# NTP version in request
MODE = 7	# mode 7, private
eol = "<br>"

PACKETDATA = bytearray(8)	# current request length is 8 bytes, response is 48 bytes

PACKETDATA[0] = VERSION << 3 | MODE
PACKETDATA[1] = 0		# sequence
PACKETDATA[2] = 0x10	# implementation == 0x10, custom
PACKETDATA[3] = 1		# request code, just 1 for now

PACKETDATA[4] = 0		# unused for now
PACKETDATA[5] = 0
PACKETDATA[6] = 0
PACKETDATA[7] = 0

print binascii.hexlify(PACKETDATA)

# reference time (in seconds since 1900-01-01 00:00:00) for conversion from NTP time to system time
TIME1970 = 2208988800L

# Create a UDP socket
server_address = (IPADDR, 123)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2.5)

# Send request
sent = sock.sendto(PACKETDATA, server_address)

# Receive response
RX_PACKET, server = sock.recvfrom(1024)
print binascii.hexlify(RX_PACKET)

ref_ts0 	=(struct.unpack('<I',RX_PACKET[16:20])[0]) / 4294967296.0	# fractional part of the NTP timestamp
ref_ts1 	= struct.unpack('<I',RX_PACKET[20:24])[0]	# full seconds of NTP timestamp
uptime 		= struct.unpack('<I',RX_PACKET[24:28])[0]
NTP_served 	= struct.unpack('<I',RX_PACKET[28:32])[0]
CMD_served	= struct.unpack('<I',RX_PACKET[32:36])[0]
lock_time	= struct.unpack('<I',RX_PACKET[36:40])[0]
flags 		= struct.unpack( 'B',RX_PACKET[40])[0]
numSV 		= struct.unpack( 'B',RX_PACKET[41])[0]
ser_num 	= struct.unpack('<H',RX_PACKET[42:44])[0]	
FW_ver 		= struct.unpack('<I',RX_PACKET[44:48])[0]

t = time.gmtime(ref_ts1 - TIME1970)

# actual statistics received from the server
#print "NTP server IP address:", IPADDR
#print eol
print ("UTC time: %d-%02d-%02d %02d:%02d:%02.0f" % (t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec + ref_ts0))

print ("NTP time: %02.0f" % (ref_ts1 + ref_ts0))

#derived statistics
print ("Average load since restart: %02.0f requests per second" % (1.0 * NTP_served / uptime))

print "NTP requests served:", NTP_served

print "Mode 6 requests served:", CMD_served

print "Uptime:", uptime, "seconds (", uptime/86400, "days )"

print "GPS lock time:", lock_time, "seconds (", lock_time/86400, "days )"

#print "GPS flags:", flags
print "Active satellites:", numSV

print ("Firmware version: %x.%02x" % (FW_ver>>8, FW_ver&0xFF))

print "Serial number:", ser_num



#print NTP_served
#print NTP_served
#print uptime
#print "LeoNTP requests"

#print "rrdtool update ntp1.rrd ", ref_ts1 - TIME1970, ":", NTP_served

#print ("rrdtool update ntp1.rrd  %d:%d" % (ref_ts1 - TIME1970, NTP_served))

sock.close()
