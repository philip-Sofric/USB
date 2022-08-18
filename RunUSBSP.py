from ctypes import *
import matplotlib.pyplot as plt
import numpy as np

dll_path = 'bwtekusb.dll'
add_lib = CDLL(dll_path)
# print('Successfully added library ', add_lib)

USBtype = c_int(0)
Channel = c_int(0)

OutFileEEPROM = c_wchar_p('para.ini')
print(OutFileEEPROM.value)

TimingMode = c_int(0)
PixelNum = 512
InputMode = c_int(0)
Param = c_int(0)

IntegrationTime = c_long(5)
data_array = (c_ushort * PixelNum)()
trigger = c_int(0)

Command = c_int(0x10)
ADValue = c_int(0)
Temperature = c_double(0.00)
LE = 4
CCode = (c_byte * LE)()

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

    return_on_settime = add_lib.bwtekSetTimeUSB(IntegrationTime, Channel)
    print('Integration time is {} ms'.format(return_on_settime))

    return_on_dataRead = add_lib.bwtekDataReadUSB(trigger, byref(data_array), Channel)
    DT = []
    if return_on_dataRead == PixelNum:
        for j in range(PixelNum):
            DT.append(data_array[j])
    xarray = np.arange(0, PixelNum, 1)
    plt.plot(xarray, DT)

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
return_on_closeUSB = add_lib.bwtekCloseUSB(Channel)
if return_on_closeUSB:
    print('USB device is disconnected.')
add_lib.CloseDevices()

plt.show()