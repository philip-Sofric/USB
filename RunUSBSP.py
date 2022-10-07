from ctypes import *
import matplotlib.pyplot as plt
import numpy as np
from spectrotestfunctions import *

dll_path = 'bwtekusb.dll'
add_lib = CDLL(dll_path)
# print('Successfully added library ', add_lib)

USBtype = c_int(0)
Channel = c_int(0)

OutFileEEPROM = c_wchar_p('para.ini')
# print(OutFileEEPROM.value)

TimingMode = c_int(0)
PixelNum = 512
InputMode = c_int(0)
Param = c_int(0)

IntegrationTime = 1000
data_array = (c_ushort * PixelNum)()
trigger = c_int(0)

Command = c_int(0x10)
ADValue = c_int(0)
Temperature = c_double(0.00)
LE = 4
CCode = (c_byte * 10)()
modelname = (c_byte * 10)()
IPSSN = (c_byte * 10)()
IPSWL = (c_byte * 10)()

return_on_initial = add_lib.InitDevices()
if not return_on_initial:
    print('initialization fails. ')
else:
    print('initialization is successful. \n ')

    # gettype = add_lib.GetUSBType(byref(USBtype), Channel)
    # print('USB type is ', USBtype.value)

    getEEPROM = add_lib.bwtekReadEEPROMUSB('para.ini', Channel)

    return_on_test = add_lib.bwtekTestUSB(TimingMode, PixelNum, InputMode, Channel, Param)
    if return_on_test >= 0:
        print('Return of bwtekTestUSB is successful.\n')

    return_on_settime = add_lib.bwtekSetTimeUSB(IntegrationTime * 100, Channel)
    print('Integration time is {} ms'.format(return_on_settime / 100))

    return_on_dataRead = add_lib.bwtekDataReadUSB(trigger, byref(data_array), Channel)
    DT = []
    if return_on_dataRead == PixelNum:
        for j in range(PixelNum):
            DT.append(data_array[j])
    xarray = np.arange(0, PixelNum, 1)
    # plt.plot(xarray, DT)

    # return_on_stop = add_lib.bwtekStopIntegration(Channel)
    # if return_on_stop:
    #     print('Stop integration is successful')

    # return_on_temperature = add_lib.bwtekReadTemperature(Command, byref(ADValue), byref(Temperature), Channel)
    # if return_on_temperature:
    #     print('Temperature is ', Temperature.value)
    # else:
    #     print('This device has no temperature reading')

    # return_on_ccode = add_lib.GetCCode(byref(CCode), Channel)
    # cc = ''
    # for i in range(LE):
    #     cc += chr(CCode[i])
    # print(cc)
#
IPSLaser1 = 0x14  # 860
IPSLaser2 = 0x15  # 1064
setIPSlaserAdd = add_lib.bwtekSetIPSLaserAddress(IPSLaser2, Channel)
if setIPSlaserAdd > 0:
    print('Laser is set to 1064')
else:
    print('IPS 0x15-1064 not found')

#
getlaserinfo = add_lib.bwtekGetIPSLaserInfo(Channel)
if getlaserinfo > 0:
    print('IPS laser is detected')
else:
    print('No IPS laser')
#
getlasermodelname = add_lib.bwtekGetIPSLaserModelName(byref(modelname), Channel)
IPSLaserModel = ''
if getlasermodelname > 0:
    for i in np.arange(0, 10, 1):
        if modelname[i] >= 32:
            IPSLaserModel += chr(modelname[i])
        # elif modelname[i] == 32:
        #     continue
        else:
            break
    print('IPS model is ', IPSLaserModel)
else:
    print('getting model name fails')

getIPSSN = add_lib.bwtekGetIPSLaserSerialNo(byref(IPSSN), Channel)
IPSLaserSN = ''
if getIPSSN > 0:
    for i in np.arange(0, 10, 1):
        if IPSSN[i] != 0:
            IPSLaserSN += chr(IPSSN[i])
        else:
            break
    IPSLaserSN = int(IPSLaserSN)
    print('IPS laser serial number is ', IPSLaserSN)

else:
    print('getting IPS laser SN fails')
#
getIPSWL = add_lib.bwtekGetIPSLaserWavelength(byref(IPSWL), Channel)
IPSLaserWL = ''
if getIPSWL > 0:
    for i in np.arange(0, 10, 1):
        if IPSWL[i] != 0:
            IPSLaserWL += chr(IPSWL[i])
        else:
            break

    IPSLaserWL = float(IPSLaserWL)
    print(f'IPS laser wavelength is {IPSLaserWL}')

# this is to set laser power percentage
duty = 0
issetlp = add_lib.bwtekSetIPSLaserPWMDuty(duty, Channel)
if issetlp > 0:
    print('setting laser power successfully.')
else:
    print('setting laser power fails.')

# this is to enable/disable laser operation
Enable = 1
getIPSStatus = add_lib.bwtekSetIPSLaserEnable(Enable, Channel)
if getIPSStatus:
    print('Laser is enabled')
else:
    print('laser is not enabled')

# this is to enable/disable PWM mode
enablePWM = add_lib.bwtekSetIPSLaserPWMEnable(Enable, Channel)
if enablePWM:
    print('Digital mode is enabled')
else:
    print('Digital mode is not enabled')

add_lib.bwtekSetIPSLaserPWMDuty(100)

# add_lib.bwtekSetIPSLaserPWMDuty(0)

# this is to get laser power
LP = add_lib.bwtekGetIPSLaserPower(Channel)
print(f'laser power is {LP}')

# getlaserchannel = add_lib.GetLaserChannel()
# if getlaserchannel >= 0:
#     print('Cleanlaze is detected')
# else:
#     print('No Cleanlaze laser')

#
# return_on_closeUSB = add_lib.bwtekCloseUSB(Channel)
# if return_on_closeUSB:
#     print('USB device is disconnected.')
# add_lib.CloseDevices()
#
# plt.show()
