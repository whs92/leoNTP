TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#==================================================
# build a support library

LIBRARY_IOC += leoNTP

# xxxRecord.h will be created from xxxRecord.dbd
#DBDINC += xxxRecord
# install leoNTP.dbd into <top>/dbd
DBD += leoNTP.dbd

# specify all source files to be compiled and added to the library
#leoNTP_SRCS += xxx

leoNTP_LIBS += $(EPICS_BASE_IOC_LIBS)

#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

