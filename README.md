# leoNTP
EPICS support module using stream device which exposes the status of the leoNTP server. Based on code supplied by leoNTP (http://www.leontp.com/firmware/) 

In st.cmd include

drvAsynIPPortConfigure("leoNTP","$(IP):123 UDP")
dbLoadRecords("../../db/leoNTP.db")#

where $(IP) is the IP address of the leoNTP server

https://store.uputronics.com/index.php?route=product/product&product_id=92 
