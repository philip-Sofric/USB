# wrapper of functions from SDK

from ctypes import *
import global_variables
from std_functions import *

dll_path = 'bwtekusb.dll'
RS_path = r'C:\Users\4510042\PycharmProjects\USB\bwtekrs.dll'
add_lib = CDLL(dll_path)
add_librs = CDLL(RS_path)


def SP_initialize():
    isInitialized = -1
    if global_variables.InterfaceType == 0:
        isInitialized = add_lib.InitDevices()
        # return is True or False
    elif global_variables.InterfaceType == 1:
        isInitialized = add_librs.bwtekInitPortRS232(global_variables.comport,
                                                     global_variables.baudrate,
                                                     global_variables.Channel)
        # return is positive value or non-positive
    return isInitialized


def SP_EEPROM():
    getEEPROM = -1
    if global_variables.InterfaceType == 0:
        getEEPROM = add_lib.bwtekReadEEPROMUSB(b'para.ini', global_variables.Channel)
    elif global_variables.InterfaceType == 1:
        getEEPROM = add_librs.bwtekReadEEPROMRS232(b'para.ini', global_variables.Channel)
    return getEEPROM


def SP_EEPROM_write(parafile):
    setEEPROM = -1
    if global_variables.InterfaceType == 0:
        setEEPROM = add_lib.bwtekWriteEEPROMUSB(bytes(parafile, encoding='utf8'), global_variables.Channel)
    elif global_variables.InterfaceType == 1:
        setEEPROM = add_librs.bwtekWriteEEPROMRS232(bytes(parafile, encoding='utf8'), global_variables.Channel)
    return setEEPROM


def SP_test():
    isTested = -1
    if global_variables.InterfaceType == 0:
        # print('Pixel num ', global_variables.PixelNum)
        isTested = add_lib.bwtekTestUSB(global_variables.TimingMode,
                                        global_variables.PixelNum,
                                        global_variables.InputMode,
                                        global_variables.Channel,
                                        global_variables.Param)
    elif global_variables.InterfaceType == 1:
        isTested = add_librs.bwtekTestRS232(global_variables.TimingMode,
                                            global_variables.PixelNum,
                                            global_variables.InputMode,
                                            global_variables.Channel)
    return isTested


def Get_Detector_Temp():
    isgetDETTemp = -1
    if global_variables.InterfaceType == 0:
        isgetDETTemp = add_lib.bwtekReadTemperature(global_variables.Command1,
                                                    byref(global_variables.ADValue),
                                                    byref(global_variables.getTemperature1),
                                                    global_variables.Channel)
    elif global_variables.InterfaceType == 1:
        isgetDETTemp = add_librs.bwtekReadTemperatureRS232(global_variables.nMuxOut,
                                                           byref(global_variables.ADValue),
                                                           byref(global_variables.getTemperature1),
                                                           global_variables.Channel)
    return isgetDETTemp


def Get_Ambient_Temp():
    isgetAMTemp = -1
    if global_variables.InterfaceType == 0:
        isgetAMTemp = add_lib.bwtekReadTemperature(global_variables.Command2,
                                                   byref(global_variables.ADValue),
                                                   byref(global_variables.getTemperature2),
                                                   global_variables.Channel)
    elif global_variables.InterfaceType == 1:
        isgetAMTemp = add_librs.bwtekReadTemperature()
    return isgetAMTemp


def Set_Detector_Temp(setvalue):
    issetDETTemp = -1
    if global_variables.InterfaceType == 0:
        issetDETTemp = add_lib.bwtekSetTemperatureUSB(global_variables.DAChannel1,
                                                      setvalue,
                                                      global_variables.Channel)
    elif global_variables.InterfaceType == 1:
        issetDETTemp = add_librs.bwtekSetTemperatureRS232(global_variables.DAChannel1,
                                                          setvalue,
                                                          global_variables.Channel)
    return issetDETTemp


def Set_Ambient_Temp(setvalue):
    issetAMTemp = -1
    if global_variables.InterfaceType == 0:
        issetAMTemp = add_lib.bwtekSetTemperatureUSB(global_variables.DAChannel2,
                                                     setvalue,
                                                     global_variables.Channel)
    elif global_variables.InterfaceType == 1:
        issetAMTemp = add_librs.bwtekSetTemperatureRS232(global_variables.DAChannel2,
                                                         setvalue,
                                                         global_variables.Channel)
    return issetAMTemp


def Set_Gain(setvalue):
    issetGain = -1
    if global_variables.InterfaceType == 0:
        issetGain = add_lib.bwtekSetAnalogOut(global_variables.pin_set_gain,
                                              int(setvalue),
                                              global_variables.Channel)
    elif global_variables.InterfaceType == 1:
        issetGain = add_librs.bwtekSetAnalogOutRS232(global_variables.pin_set_gain,
                                                     setvalue,
                                                     global_variables.Channel)
    return issetGain


def Set_Offset(setvalue):
    issetOffset = -1
    if global_variables.InterfaceType == 0:
        issetOffset = add_lib.bwtekSetAnalogOut(global_variables.pin_set_offset,
                                                setvalue,
                                                global_variables.Channel)
    elif global_variables.InterfaceType == 1:
        issetOffset = add_librs.bwtekSetAnalogOutRS232(global_variables.pin_set_offset,
                                                       setvalue,
                                                       global_variables.Channel)
    return issetOffset


def Set_Time(setvalue):
    issetTime = -1
    if global_variables.InterfaceType == 0:
        issetTime = add_lib.bwtekSetTimeUSB(setvalue * global_variables.time_factor,
                                            global_variables.Channel)
    elif global_variables.InterfaceType == 1:
        issetTime = add_librs.bwtekSetTimeRS232(int(setvalue * global_variables.time_factor),
                                                global_variables.Channel)
    return issetTime


def lASER_initialize():
    islaserInitialized = -1
    global_variables.LR_channel = add_lib.GetLaserChannel()
    # USB laser has specific channel other than spectrometer
    if global_variables.InterfaceType == 0 and global_variables.LR_channel >= 0:
        islaserInitialized = add_lib.bwtekinitializeLC(0, global_variables.LR_channel)
        if islaserInitialized > 0:
            global_variables.LaserType = 1
    # IPS laser connected through I2C to USB spectrometer
    elif global_variables.InterfaceType == 0 and add_lib.bwtekGetIPSLaserInfo(global_variables.Channel) > 0:
        islaserInitialized = add_lib.bwtekGetIPSLaserInfo(global_variables.Channel)
        global_variables.LaserType = 2
    # HHEX: IPS laser connected through I2C to RS232 spectrometer
    elif global_variables.InterfaceType == 1 and add_librs.bwtekInitLaserRS232(global_variables.Channel) > 0:
        islaserInitialized = add_librs.bwtekInitLaserRS232(global_variables.Channel)
        global_variables.LaserType = 3
    else:
        global_variables.LaserType = 0
    return islaserInitialized


def Set_Laser(addr):
    if addr == 0x14:
        add_lib.bwtekSetTTLOut(1, 1, 0, global_variables.Channel)
    elif addr == 0x15:
        add_lib.bwtekSetTTLOut(1, 0, 0, global_variables.Channel)
    else:
        pass
    issetIPSlaser = add_lib.bwtekSetIPSLaserAddress(addr, global_variables.Channel)
    return issetIPSlaser


def Get_All_LaserInfo(addr):
    length = 10
    _IPSModel = (c_byte * length)()
    _IPSSN = (c_byte * length)()
    _IPSWL = (c_byte * length)()
    _IPSVersion = (c_byte * length)()
    if Set_Laser(addr) > 0:
        add_lib.bwtekGetIPSLaserInfo(global_variables.Channel)
        # add_lib.bwtekGetIPSLaserModelName(byref(_IPSModel), global_variables.Channel)
        # global_variables.IPSModel = convertASCII2string(_IPSModel, length)
        # add_lib.bwtekGetIPSLaserSerialNo(byref(_IPSSN), global_variables.Channel)
        # global_variables.IPSSN = convertASCII2string(_IPSSN, length)
        add_lib.bwtekGetIPSLaserWavelength(byref(_IPSWL), global_variables.Channel)
        global_variables.IPSWL = convertASCII2string(_IPSWL, length)
        # IPSLaserWL = ''
        # for i in np.arange(0, length, 1):
        #     if 32 <= _IPSWL[i] <= 126:
        #         IPSLaserWL += chr(_IPSWL[i])
        #     else:
        #         break
        # global_variables.IPSWL = IPSLaserWL
        # add_lib.bwtekGetIPSLaserProductVersion(byref(_IPSVersion), global_variables.Channel)
        # global_variables.IPSVersion = convertASCII2string(_IPSVersion, length)
    # print('Laser wavelength is ', global_variables.IPSWL)


def Set_Laser_Power(pctg):
    if global_variables.LaserType == 1:
        add_lib.bwtekSetDACLC(4, 4095, 0)
    elif global_variables.LaserType == 2:

        add_lib.bwtekSetIPSLaserPWMDuty(0, global_variables.Channel)

        add_lib.bwtekSetIPSLaserPWMEnable(1, global_variables.Channel)
        add_lib.bwtekSetIPSLaserEnable(1, global_variables.Channel)
        isLaserpowerset = add_lib.bwtekSetIPSLaserPWMDuty(pctg, global_variables.Channel)
        # if isLaserpowerset == 1:
        #     print('The actual laser power is ', pctg.value)
        # else:
        #     print('Laser power set fails')
        # bwtekGetIPSLaserCurrent
    elif global_variables.LaserType == 3:
        pass
    else:
        pass


def Get_IPSLaser_Power():
    return add_lib.bwtekGetIPSLaserPower(global_variables.Channel)


def Get_IPSLaser_PWMDuty():
    return add_lib.bwtekGetIPSLaserPWMDuty(global_variables.Channel)


def Close_Laser():
    if global_variables.LaserType == 1:
        pass
    elif global_variables.LaserType == 2:
        add_lib.bwtekSetIPSLaserEnable(0, global_variables.Channel)
    elif global_variables.LaserType == 3:
        pass
    else:
        pass


# ydata_array is (c_ushort * global_variables.PixelNum)()
def Get_Data():
    data_array = (c_ushort * global_variables.PixelNum)()
    isDataReadSuccessful = -1
    if global_variables.InterfaceType == 0:
        isDataReadSuccessful = add_lib.bwtekDataReadUSB(global_variables.trigger, byref(data_array),
                                                        global_variables.Channel)
    elif global_variables.InterfaceType == 1:
        isDataReadSuccessful = add_librs.bwtekDataReadRS232(global_variables.trigger, byref(data_array),
                                                            global_variables.Channel)
    # reverse data if applicable
    if isDataReadSuccessful == global_variables.PixelNum:
        if global_variables.ReverseX == 1:
            data_array = data_array[::-1]
        if global_variables.ReverseY == 1:
            data_array = np.ones(global_variables.PixelNum, ) * 65535 - data_array
        return data_array
    else:
        return []
