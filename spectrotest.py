import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as fd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import time
from SDKfunctions import *
import global_variables

datapath = r'C:\Users\4510042\PycharmProjects\USB\Data'
dll_path = 'bwtekusb.dll'
RS_path = r'C:\Users\4510042\PycharmProjects\USB\bwtekrs.dll'
add_lib = CDLL(dll_path)
add_librs = CDLL(RS_path)


def param_config(parafile):
    # parameters from para.ini
    global_variables.PixelNum = getPixelNumfromEEPROM(parafile)
    global_variables.Model = getModelfromEEPROM(parafile)
    global_variables.SpectrometerType = getSPTypefromEEPROM(parafile)
    global_variables.TimingMode = getTimingModefromEEPROM(parafile)
    global_variables.InputMode = getInputModefromEEPROM(parafile)
    global_variables.LEW = getLaserwavelengthfromEEPROM(parafile)
    global_variables.gain = getGainfromEEPROM(parafile)
    global_variables.offset = getOffsetfromEEPROM(parafile)
    # global_variables.a_coff = geta_coeffromEEPROM('p')
    global_variables.a_coff = [1.03746166e+03, 9.01004426e-01, -6.01681827e-04, 1.84154643e-06]
    global_variables.ReverseX, global_variables.ReverseY = getReversefromEEPROM(parafile)
    # global_variables.ReverseX = 1
    global_variables.pixel_array = np.arange(0, global_variables.PixelNum, 1)
    global_variables.data_P_array = (c_ushort * global_variables.PixelNum)()
    # parameters by SP model
    if global_variables.Model == 'BTC284N' or 'BTC284C':
        global_variables.Command1 = 0x41
        global_variables.Command2 = 0x42
        global_variables.DAChannel1 = 1
        global_variables.DAChannel2 = 2
        global_variables.detector_temperature_array = [-25]
        global_variables.chamber_temperature_array = [20]
        global_variables.integration_time_array = [1000, 5000, 10000]
        global_variables.time_factor = 100
        global_variables.pin_set_gain = 5
        global_variables.pin_set_offset = 4
    elif global_variables.Model == 'BTC281Y':
        global_variables.Command1 = 0x61
        global_variables.Command2 = 0x62
        global_variables.detector_temperature_array = [-25]
        global_variables.chamber_temperature_array = [20]
        global_variables.integration_time_array = [1000, 5000, 10000]
    elif global_variables.Model == 'HHEX':
        global_variables.time_factor = 0.1


def setInterface():
    TT = interfacetype.get()
    global_variables.InterfaceType = int(TT) - 1
    # print(f'Interface type is {global_variables.InterfaceTypes[global_variables.InterfaceType]}')
    if global_variables.InterfaceType == 0:
        button_Test['text'] = 'TestUSB'
        button_initialize['state'] = 'normal'
        label_comPort.place_forget()
        textbox_comport.place_forget()
    elif global_variables.InterfaceType == 1:
        button_Test['text'] = 'TestRS232'
        button_initialize['state'] = 'normal'
        label_comPort.place(x=550, y=10)
        textbox_comport.place(x=650, y=10)
    else:
        button_Test['text'] = 'TestNull'
        button_initialize['state'] = 'disabled'
        label_comPort.place_forget()
        textbox_comport.place_forget()


def initialization():
    global_variables.comport = comPort.get()
    label_initialize = ttk.Label(tab_functions)
    label_initialize.place(x=250, y=40)
    if SP_initialize() > 0:
        label_initialize['text'] = 'device is initialized'
        button_readEEPROM['state'] = 'normal'
        button_writeEEPROM['state'] = 'normal'
    else:
        label_initialize['text'] = 'device initialization fails'
        button_readEEPROM['state'] = 'disabled'


def readEEPROM():
    label_EEPROM = ttk.Label(tab_functions)
    label_EEPROM.place(x=250, y=70)
    if SP_EEPROM() > 0:
        param_config('para.ini')
        # print('Model is', global_variables.Model)
        label_EEPROM.config(text=f'EEPROM reading is successful. Model is {global_variables.Model}')
        # Operations on Tkinter widgets
        button_Test['state'] = 'normal'
        textbox_gain.insert(0, str(global_variables.gain))
        textbox_offset.insert(0, str(global_variables.offset))
    else:
        button_Test['state'] = 'disabled'
        label_EEPROM['text'] = 'EEPROM reading fails'


def writeEEPROM():
    label_EEPROM_write = ttk.Label(tab_functions)
    label_EEPROM_write['text'] = ''
    label_EEPROM_write.place_forget()
    filetypes = (('text file', '*.txt'), ('ini file', '*.ini'), ('all files', '*.*'))
    filename = fd.askopenfilename(title='Open a file',
                                  initialdir=r'C:\Users\4510042\PycharmProjects\USB',
                                  filetypes=filetypes)
    if SP_EEPROM_write(filename) > 0:
        label_EEPROM_write.config(text=f'EEPROM writing is successful. Please read flash again!')
    else:
        label_EEPROM_write['text'] = 'EEPROM writing fails.'
    # label_EEPROM_write['text'] = SP_EEPROM_write(filename)
    label_EEPROM_write.place(x=250, y=460)


def test():
    label_test.place(x=250, y=100)
    if SP_test() > 0:
        label_test['text'] = 'Device is ready'
        button_inttime['state'] = 'normal'
        label_inttime.place(x=220, y=370)
        textbox_inttime.place(x=350, y=370)
        button_inttime_concate1['state'] = 'normal'
        button_inttime_concate2['state'] = 'normal'
        button_scan['state'] = 'normal'
        button_scan2['state'] = 'normal'
        button_close['state'] = 'normal'
        button_monitor['state'] = 'normal'

        if global_variables.Model.startswith('BTC26') or global_variables.Model.startswith('BTC28'):
            button_GetInGaAsMode['state'] = 'normal'
            button_SetInGaAsMode['state'] = 'normal'
            listbox_IGA.place(x=500, y=160)
        if global_variables.Model in global_variables.modelwith2stagecooling:
            button_readTemperature1['state'] = 'normal'
            button_readTemperature2['state'] = 'normal'
            button_setTemperature1['state'] = 'normal'
            button_setTemperature2['state'] = 'normal'
            label_setDetectorT.place(x=250, y=250)
            textbox_setDetectorTemp.place(x=400, y=250)
            label_setChamberT.place(x=250, y=280)
            textbox_setChamberTemp.place(x=400, y=280)
        if global_variables.Model in global_variables.modelwithCDC:
            # button_readGain_Offset['state'] = 'normal'
            button_setGain_Offset['state'] = 'normal'
            label_gain.place(x=250, y=340)
            textbox_gain.place(x=350, y=340)
            label_offset.place(x=450, y=340)
            textbox_offset.place(x=550, y=340)
            button_CDC['state'] = 'normal'
    else:
        label_test['text'] = 'Communication error'


def getInGaAsMode():
    label_getIGA = ttk.Label(tab_functions)
    label_getIGA.place(x=250, y=100)
    add_lib.bwtekGetInGaAsMode(byref(global_variables.getModeValue), global_variables.Channel)
    if global_variables.getModeValue.value == 0:
        label_getIGA['text'] = 'InGaAs mode is high sensitivity'
    elif global_variables.getModeValue.value == 1:
        label_getIGA['text'] = 'InGaAs mode is high dynamic range'
    else:
        label_getIGA['text'] = 'unable to get InGaAs working mode'


def setIGAValue():
    selected_index = listbox_IGA.curselection()[0]
    global_variables.setModelValue = c_int(selected_index)


def setInGaAsMode():
    label_setIGA = ttk.Label(tab_functions)
    label_setIGA.place(x=250, y=130)
    add_lib.bwtekSetInGaAsMode(global_variables.setModelValue, global_variables.Channel)
    getInGaAsMode()
    if global_variables.setModelValue.value == 0:
        label_setIGA['text'] = 'InGaAs mode is set high sensitivity'
    elif global_variables.setModelValue.value == 1:
        label_setIGA['text'] = 'InGaAs mode is set high dynamic range'
    else:
        label_setIGA['text'] = 'Wrong'


def getTemperature_stage1():
    label_getTemp1 = ttk.Label(tab_functions)
    label_getTemp1.place(x=250, y=160)
    if Get_Detector_Temp() > 0:
        label_getTemp1['text'] = f'Detector temperature is {global_variables.getTemperature1.value:6.4}'
    else:
        label_getTemp1['text'] = 'Detector temperature reading fails'


def getTemperature_stage2():
    label_getTemp2 = ttk.Label(tab_functions)
    label_getTemp2.place(x=250, y=190)
    if Get_Ambient_Temp() > 0:
        label_getTemp2['text'] = f'Chamber temperature is {global_variables.getTemperature2.value:6.4}'
    else:
        label_getTemp2['text'] = 'Chamber temperature reading fails'


def setTemperature_stage1():
    global_variables.setTemperature1 = int(setDetectorT.get())
    # print('DAC is ', global_variables.DAChannel1)
    if Set_Detector_Temp(global_variables.setTemperature1) > 0:
        print('Set detector temperature successful')
    else:
        print('Setting detector temperature fails')
    # time.sleep(5)
    getTemperature_stage1()


def setTemperature_stage2():
    global_variables.setTemperature2 = int(setChamberT.get())
    if Set_Ambient_Temp(global_variables.setTemperature2) > 0:
        print('Set chamber temperature successful')
    else:
        print('Set chamber temperature failed')
    # time.sleep(5)
    getTemperature_stage2()


def getGainOffset():
    pass


def setGainOffset():
    global_variables.gain = int(gaintext.get())
    global_variables.offset = int(offsettext.get())
    print('gain ', global_variables.gain)
    print('offset ', global_variables.offset)
    Set_Gain(global_variables.gain)
    Set_Offset(global_variables.offset)


def setIntegrationTime():
    global_variables.integration_time = int(inttimetext.get())
    Set_Time(global_variables.integration_time)
    print(f'Integration time is set to {global_variables.integration_time} ms')


def initializeLaser():
    t = lASER_initialize()
    label_initializeLaser['text'] = global_variables.LaserTypes[global_variables.LaserType]
    LP.set('0')
    if t > 0 and global_variables.LaserType == 1:
        # cleanlaze power set to 0
        global_variables.laser_power = c_double(0.0)
        radio_laser_0.place(x=50, y=40)
        radio_laser_1.place(x=200, y=40)
        radio_laser_2.place_forget()

    elif t > 0 and global_variables.LaserType == 2:
        # set power to 0
        global_variables.laser_power = c_double(0.0)
        global_variables.laser_power2 = c_double(0.0)
        Set_Laser(0x14)
        Set_Laser_Power(global_variables.laser_power)
        Set_Laser(0x15)
        Set_Laser_Power(global_variables.laser_power2)
        radio_laser_0.place(x=50, y=40)
        radio_laser_1.place(x=200, y=40)
        radio_laser_2.place(x=300, y=40)
        Get_All_LaserInfo(global_variables.IPSLaser1)
        Get_All_LaserInfo(global_variables.IPSLaser2)
    else:
        radio_laser_1.place_forget()
        radio_laser_2.place_forget()


def SetLaser():
    lo = laseroption.get()
    lo = int(lo)
    if lo == 0:
        LP.set('0')
        if global_variables.LaserType == 1:
            pass  # cleanlaze power set to 0
        if global_variables.LaserType == 2:
            # turn off both lasers but not change laser power values
            Set_Laser(global_variables.IPSLaser1)
            Set_Laser_Power(c_double(0.0))
            Set_Laser(global_variables.IPSLaser2)
            Set_Laser_Power(c_double(0.0))
            global_variables.laser_power = c_double(0.0)
        button_setLP['state'] = 'disabled'
        label_getIPSLaserAddress.place_forget()
        label_getIPSLaserLEW.place_forget()
        label_getIPSLaserPWMDuty.place_forget()
        label_getIPSLaserPower.place_forget()
    elif lo == 1:
        if global_variables.LaserType == 1:
            pass  # Cleanlaze
        elif global_variables.LaserType == 2:
            global_variables.IPSLaserAdd = 20  # 860nm
        else:
            pass
    elif lo == 2:
        global_variables.IPSLaserAdd = 21  # 1064nm
    else:
        pass
    if lo == 1 or lo == 2:
        button_setLP['state'] = 'normal'
        Set_Laser(global_variables.IPSLaserAdd)
        Get_All_LaserInfo(global_variables.IPSLaserAdd)
        label_getIPSLaserAddress['text'] = global_variables.IPSLaserAdd
        global_variables.LEW = float(global_variables.IPSWL)
        label_getIPSLaserLEW['text'] = str(global_variables.LEW)
        # print(global_variables.LEW)
        # add_lib.bwtekSetIPSLaserFactorySetting2PowerUpSetting(0)
        label_getIPSLaserPWMDuty['text'] = str(Get_IPSLaser_PWMDuty())
        label_getIPSLaserPower['text'] = str(Get_IPSLaser_Power())
        # remove existing texts
        label_getIPSLaserAddress.place_forget()
        label_getIPSLaserLEW.place_forget()
        label_getIPSLaserPWMDuty.place_forget()
        label_getIPSLaserPower.place_forget()

        # show new texts
        label_getIPSLaserAddress.place(x=50, y=70)
        label_getIPSLaserLEW.place(x=46, y=100)
        label_getIPSLaserPWMDuty.place(x=46, y=130)
        label_getIPSLaserPower.place(x=46, y=160)


# for acquisition
def Config_Laser():
    lo2 = laseroption2.get()
    lo2 = int(lo2)

    if lo2 == 0:
        label_laser1.place_forget()
        textbox_inttime_concate2.place_forget()
        label_inttime_concate2.place_forget()
        button_inttime_concate2.place_forget()
        label_laser2.place_forget()
        textbox_laserpower2a.place_forget()
        textbox_laserpower2b.place_forget()
        check_showconcat.place_forget()
        label_concat.place_forget()
        textbox_concat.place_forget()
    elif lo2 == 1:
        if global_variables.LaserType == 2:
            Set_Laser(global_variables.IPSLaserAdd)
            Get_All_LaserInfo(global_variables.IPSLaserAdd)
            global_variables.LEW = float(global_variables.IPSWL)
        else:
            pass
        textbox_inttime_concate2.place_forget()
        label_inttime_concate2.place_forget()
        button_inttime_concate2.place_forget()
        label_laser2.place_forget()
        textbox_laserpower2b.place_forget()
        check_showconcat.place_forget()
        label_concat.place_forget()
        textbox_concat.place_forget()
        label_laser1['text'] = f'LEW {global_variables.LEW}, laser power at (%)'
        label_laser1.place(x=10, y=100)
        textbox_laserpower2a.place(x=180, y=100)
    elif lo2 == 2:
        if global_variables.LaserType == 2:
            Set_Laser(21)
            Get_All_LaserInfo(21)
            global_variables.LEW = float(global_variables.IPSWL)
            Set_Laser(20)
            Get_All_LaserInfo(20)
            global_variables.LEW2 = float(global_variables.IPSWL)
        else:
            pass
        label_inttime_concate2.place(x=10, y=40)
        textbox_inttime_concate2.place(x=150, y=40)
        button_inttime_concate2.place(x=250, y=40)
        label_laser1['text'] = f'LEW {global_variables.LEW}, laser power at (%)'
        label_laser1.place(x=10, y=100)
        label_laser2['text'] = f'LEW {global_variables.LEW2}, laser power at (%)'
        label_laser2.place(x=10, y=130)
        textbox_laserpower2a.place(x=180, y=100)
        textbox_laserpower2b.place(x=180, y=130)
        check_showconcat.place(x=30, y=580)
        label_concat.place(x=30, y=610)
        textbox_concat.place(x=180, y=610)


def getLaserWL():
    pass


def setLaserPower():
    global_variables.laser_power.value = float(LP.get())
    print('Laser power to be set is ', global_variables.laser_power.value)
    Set_Laser_Power(global_variables.laser_power)


def closeLaser():
    Close_Laser()


def scan():
    # set integration time and laser power
    global_variables.integration_time = int(inttimetext.get())
    Set_Time(global_variables.integration_time)
    global_variables.laser_power.value = float(LP.get())
    Set_Laser_Power(global_variables.laser_power)
    # obtain pixel array and data array
    global_variables.pixel_array = np.arange(0, global_variables.PixelNum, 1)
    global_variables.data_P_array = Get_Data()
    if len(global_variables.data_P_array):
        figure = Figure(figsize=(6, 3), dpi=100)
        display = figure.add_subplot()
        display.set_title('Spectrum')
        display.set_xlabel('Pixel')
        display.set_ylabel('Intensity')
        display.set_xlim(0, 600)
        display.set_ylim(0, 65535)
        canvas = FigureCanvasTkAgg(figure, master=tab_functions)
        canvas.get_tk_widget().place(x=650, y=250)
        display.plot(global_variables.pixel_array, global_variables.data_P_array)
        canvas.draw()


def multiscan():
    pass


def scan2():
    # get integration time and laser power
    global_variables.integration_time = int(inttimetext_concate1.get())
    global_variables.integration_time2 = int(inttimetext_concate2.get())
    global_variables.laser_power.value = float(LP2a.get())
    global_variables.laser_power2.value = float(LP2b.get())
    lo2 = laseroption2.get()
    lo2 = int(lo2)
    if lo2 == 0:
        # set all laser power to 0
        lASER_initialize()
        Set_Laser(20)
        Set_Laser_Power(c_double(0))
        Set_Laser(21)
        Set_Laser_Power(c_double(0))
        # set integration time
        Set_Time(global_variables.integration_time)
        # obtain data
        global_variables.pixel_array = np.arange(0, global_variables.PixelNum, 1)
        global_variables.data_P_array = Get_Data()
        # obtain dark data
        if int(Enable_dark.get()) == 1:
            global_variables.dark_array = Get_Data()
        else:
            global_variables.dark_array = np.zeros(global_variables.PixelNum, )
        global_variables.data_P_array = global_variables.data_P_array - global_variables.dark_array
        if len(global_variables.data_P_array):
            global_variables.Wavelength_array = convertP2WL(global_variables.pixel_array,
                                                            global_variables.a_coff)
            global_variables.RamanShift_array = convertWL2RS(global_variables.Wavelength_array,
                                                             global_variables.LEW)
            start = int(global_variables.RamanShift_array[0] / 100 - 1) * 100
            end = int(global_variables.RamanShift_array[-1] / 100 + 1) * 100
            global_variables.RamanShift_array_interp = np.arange(start, end + 1, 4)
            global_variables.data_RS_array_interp = interpolation(global_variables.RamanShift_array,
                                                                  global_variables.data_P_array,
                                                                  global_variables.RamanShift_array_interp)
            # if int(Enable_dark.get()) == 1:
            #     length_dataP = len(global_variables.data_P_array)
            #     length_dataRSInterp = len(global_variables.data_RS_array_interp)
            #     global_variables.data_P_array = np.zeros(length_dataP)
            #     global_variables.data_RS_array_interp = np.zeros(length_dataRSInterp)
            SP_plot()
    elif lo2 == 1:
        # set laser power
        lASER_initialize()
        if global_variables.LaserType == 2:
            Set_Laser(global_variables.IPSLaserAdd)
            Set_Laser_Power(global_variables.laser_power)
        # set integration time
        Set_Time(global_variables.integration_time)
        # obtain data
        global_variables.pixel_array = np.arange(0, global_variables.PixelNum, 1)
        global_variables.data_P_array = Get_Data()
        # obtain dark data
        if int(Enable_dark.get()) == 1:
            Set_Laser_Power(c_double(0))
            global_variables.dark_array = Get_Data()
        else:
            global_variables.dark_array = np.zeros(global_variables.PixelNum, )
        global_variables.data_P_array = global_variables.data_P_array - global_variables.dark_array
        if len(global_variables.data_P_array):
            global_variables.Wavelength_array = convertP2WL(global_variables.pixel_array,
                                                            global_variables.a_coff)
            global_variables.RamanShift_array = convertWL2RS(global_variables.Wavelength_array,
                                                             global_variables.LEW)
            start = int(global_variables.RamanShift_array[0] / 100 - 1) * 100
            end = int(global_variables.RamanShift_array[-1] / 100 + 1) * 100
            global_variables.RamanShift_array_interp = np.arange(start, end + 1, 4)
            global_variables.data_RS_array_interp = interpolation(global_variables.RamanShift_array,
                                                                  global_variables.data_P_array,
                                                                  global_variables.RamanShift_array_interp)
            # df = pd.DataFrame(global_variables.data_P_array)
            # df.to_csv(r'C:\Users\4510042\OneDrive - Metrohm Group\Desktop\scc\ps.csv')
            SP_plot()
    elif lo2 == 2:
        # for laser 1: 1064
        # set laser power
        if global_variables.LaserType == 2:
            Set_Laser(0x14)
            Set_Laser_Power(c_double(0))
            Set_Laser(0x15)
            Set_Laser_Power(global_variables.laser_power)
        # set integration time
        Set_Time(global_variables.integration_time)
        # obtain data
        global_variables.pixel_array = np.arange(0, global_variables.PixelNum, 1)
        global_variables.data_P_array = Get_Data()
        # obtain dark data
        if int(Enable_dark.get()) == 1:
            Set_Laser_Power(c_double(0))
            global_variables.dark_array = Get_Data()
        else:
            global_variables.dark_array = np.zeros(global_variables.PixelNum, )
        global_variables.data_P_array = global_variables.data_P_array - global_variables.dark_array
        if len(global_variables.data_P_array):
            global_variables.Wavelength_array = convertP2WL(global_variables.pixel_array,
                                                            global_variables.a_coff)
            global_variables.RamanShift_array = convertWL2RS(global_variables.Wavelength_array,
                                                             global_variables.LEW)
            start = int(global_variables.RamanShift_array[0] / 100 - 1) * 100
            end = int(global_variables.RamanShift_array[-1] / 100 + 1) * 100
            global_variables.RamanShift_array_interp = np.arange(start, end + 1, 4)
            global_variables.data_RS_array_interp = interpolation(global_variables.RamanShift_array,
                                                                  global_variables.data_P_array,
                                                                  global_variables.RamanShift_array_interp)
        # for laser 2: 860
        # set laser power
        if global_variables.LaserType == 2:
            Set_Laser(0x15)
            Set_Laser_Power(c_double(0))
            Set_Laser(0x14)
            Set_Laser_Power(global_variables.laser_power2)
        # set integration time
        Set_Time(global_variables.integration_time2)
        # obtain data
        global_variables.pixel_array = np.arange(0, global_variables.PixelNum, 1)
        global_variables.data_P_array2 = Get_Data()
        # obtain dark data
        if int(Enable_dark.get()) == 1:
            Set_Laser_Power(c_double(0))
            global_variables.dark_array = Get_Data()
        else:
            global_variables.dark_array = np.zeros(global_variables.PixelNum, )
        global_variables.data_P_array2 = global_variables.data_P_array2 - global_variables.dark_array
        if len(global_variables.data_P_array2):
            global_variables.Wavelength_array2 = convertP2WL(global_variables.pixel_array,
                                                             global_variables.a_coff)
            global_variables.RamanShift_array2 = convertWL2RS(global_variables.Wavelength_array2,
                                                              global_variables.LEW2)
            start = int(global_variables.RamanShift_array2[0] / 100 - 1) * 100
            end = int(global_variables.RamanShift_array2[-1] / 100 + 1) * 100
            global_variables.RamanShift_array_interp2 = np.arange(start, end + 1, 4)
            global_variables.data_RS_array_interp2 = interpolation(global_variables.RamanShift_array2,
                                                                   global_variables.data_P_array2,
                                                                   global_variables.RamanShift_array_interp2)
        SP_plot()
    else:
        pass


def SP_plot():
    figure = Figure(figsize=(7, 5), dpi=100)
    display = figure.add_subplot()
    display.set_title('Spectrum')
    display.set_ylabel('Intensity')
    display.set_ylim(0, 65535)
    canvas = FigureCanvasTkAgg(figure, master=tab_acquisition)
    canvas.get_tk_widget().place(x=280, y=200)
    lo2 = laseroption2.get()
    lo2 = int(lo2)
    sc = show_concat.get()
    XT = int(xaxistype.get())
    if XT == 0:
        display.set_xlabel('Pixel')
        display.set_xlim(0, global_variables.PixelNum)
        display.plot(global_variables.pixel_array, global_variables.data_P_array)
        if lo2 == 2:
            display.plot(global_variables.pixel_array, global_variables.data_P_array2)
        canvas.draw()
    elif XT == 1:
        display.set_xlabel('Wavelength')
        display.set_xlim((int(global_variables.Wavelength_array[0] / 100) - 1) * 100,
                         (int(global_variables.Wavelength_array[-1] / 100) + 1) * 100)
        display.plot(global_variables.Wavelength_array, global_variables.data_P_array)
        if lo2 == 2:
            display.plot(global_variables.Wavelength_array, global_variables.data_P_array2)
        canvas.draw()
    elif XT == 2:
        display.set_xlabel('Raman Shift')
        display.set_xlim((int(global_variables.RamanShift_array[0] / 100) - 1) * 100,
                         (int(global_variables.RamanShift_array[-1] / 100) + 1) * 100)
        display.plot(global_variables.RamanShift_array, global_variables.data_P_array)
        # cannot display Raman spectrum 2 on the same plot without interpolation
        canvas.draw()
    elif XT == 3:
        display.set_xlabel('Raman Shift')
        if lo2 != 2:
            start = global_variables.RamanShift_array_interp[0]
            end = global_variables.RamanShift_array_interp[-1]
            display.set_xlim(start, end)
            display.plot(global_variables.RamanShift_array_interp, global_variables.data_RS_array_interp)
        else:
            start = min(global_variables.RamanShift_array_interp[0],
                        global_variables.RamanShift_array_interp2[0])
            end = max(global_variables.RamanShift_array_interp[-1],
                      global_variables.RamanShift_array_interp2[-1])
            display.set_xlim(start, end)
            global_variables.RamanShift_array_concat = np.arange(start, end + 1, 4)
            # length = len(global_variables.RamanShift_array_concat)
            global_variables.data_RS_array_concat = []
            if sc == 0:
                display.plot(global_variables.RamanShift_array_interp, global_variables.data_RS_array_interp)
                display.plot(global_variables.RamanShift_array_interp2, global_variables.data_RS_array_interp2)
                canvas.draw()
            elif sc == 1:
                point_concat = ConcatP.get()
                point_concat = int(int(point_concat) / 4) * 4  # round to 4
                p1 = find_index(global_variables.RamanShift_array_interp, point_concat)
                p2 = find_index(global_variables.RamanShift_array_interp2, point_concat)
                if p1 == -1:
                    print('concatenating point does not exist in 1064 data !')
                elif p2 == -1:
                    print('concatenating point does not exist in 860 data !')
                else:
                    if global_variables.RamanShift_array_interp[0] <= global_variables.RamanShift_array_interp2[0]:
                        partone = global_variables.data_RS_array_interp[:p1 + 1]
                        parttwo = global_variables.data_RS_array_interp2[p2 + 1:]
                    else:
                        partone = global_variables.data_RS_array_interp2[:p2 + 1]

                        parttwo = global_variables.data_RS_array_interp[p1 + 1:]
                    global_variables.data_RS_array_concat = np.concatenate([partone, parttwo])
                    display.plot(global_variables.RamanShift_array_concat, global_variables.data_RS_array_concat)
        canvas.draw()
    else:
        pass


def monitor():
    ct = Enable_tempmonitor.get()
    total_scans = int(num_totalscan.get())
    data_matrix = []
    timestamp_array = []
    detector_temperature_array = []
    for scan_index in range(total_scans):
        if ct:
            if Get_Detector_Temp() <= 0:
                print('Schedule is aborted due to scan error !')
                break
            else:
                timestamp_array.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                detector_temperature_array.append(global_variables.getTemperature1.value)
                if abs(global_variables.getTemperature1.value + 25) > 5:
                    print('Schedule is aborted due to detector out of spec !')
                    break
        # set integration time and laser power
        global_variables.integration_time = int(inttimetext.get())
        Set_Time(global_variables.integration_time)
        global_variables.laser_power.value = float(LP.get())
        Set_Laser_Power(global_variables.laser_power)
        # obtain pixel array and data array
        # global_variables.pixel_array = np.arange(0, global_variables.PixelNum, 1)
        global_variables.data_P_array = Get_Data()
        data_matrix.append(global_variables.data_P_array)
        time.sleep(1)
    df = pd.DataFrame(np.transpose(data_matrix))
    df.to_csv(r'C:\Users\4510042\OneDrive - Metrohm Group\Desktop\scc\datamatrix.csv', index=False)
    if len(timestamp_array) != 0:
        df2 = pd.DataFrame(
            {'Date and Time': timestamp_array,
             'Index': range(len(timestamp_array)),
             'Temperature': detector_temperature_array})
        df2.to_csv(r'C:\Users\4510042\OneDrive - Metrohm Group\Desktop\scc\temperature_array.csv', index=False)


def CDC():
    label_CDC['text'] = 'Scanning'
    # set IGA mode to high sensitivity
    add_lib.bwtekSetInGaAsMode(0, global_variables.Channel)
    os.chdir(datapath)
    _type = []
    _temperature = []
    _integration = []
    _gain = []
    _offset = []
    _std = []
    Set_Laser_Power(c_double(0))
    Set_Gain(40000)
    for temperature in global_variables.detector_temperature_array:
        Set_Laser_Power(c_double(0))
        Set_Gain(40000)
        temp_set_count = 0
        if Get_Detector_Temp():
            label_CDC['text'] = f'Initial detector temperature is {global_variables.getTemperature1.value:6.4}'
        # detector temperature stabilization
        while abs(global_variables.getTemperature1.value - temperature) > 1.0 and temp_set_count <= 20:
            Set_Detector_Temp(temperature)
            temp_set_count += 1
            # time.sleep(2)
            Get_Detector_Temp()
        if temp_set_count > 20:
            label_CDC['text'] = \
                f'Detector cannot be stabilized. Current temperature is {global_variables.getTemperature1.value} '
        else:
            label_CDC['text'] = \
                f'Stabilized temperature is {global_variables.getTemperature1.value}...\n'
        # no matter temperature is stabilized or not, calibration continues...
        label_CDC['text'] = 'Calibration starts...'
        Set_Time(200)
        Get_Data()  # this first data after temperature change is abandoned
        for Integration in global_variables.integration_time_array:
            # start offset calibration
            Set_Laser_Power(c_double(0))
            Set_Time(Integration)
            Set_Gain(40000)
            std_array = []
            df_offset = pd.DataFrame({'Pixel': np.arange(0, global_variables.PixelNum, 1)})
            for offset_value in global_variables.offset_array:
                Set_Offset(offset_value)
                yarray = Get_Data()
                std_array.append(calc_STD(yarray))
                df_offset[str(offset_value)] = yarray
            filename = str(temperature) + '_' + str(Integration) + '_' + 'offset.csv'
            df_offset.to_csv(filename, index=False)
            df_std_o = pd.DataFrame({'Offset': global_variables.offset_array, 'STD': std_array})
            optimized_offset = find_optimized_offset(df_std_o)
            _type.append('O')
            _temperature.append(temperature)
            _integration.append(Integration)
            _gain.append(40000)
            _offset.append(optimized_offset[2])
            _std.append(optimized_offset[3])
            # start gain calibration
            Set_Laser_Power(c_double(100))
            Set_Time(Integration)
            Set_Offset(optimized_offset[2])
            std_array = []
            df_gain = pd.DataFrame({'Pixel': np.arange(0, global_variables.PixelNum, 1)})
            for gain_value in global_variables.gain_array:
                Set_Gain(gain_value)
                yarray = Get_Data()
                std_array.append(calc_STD(yarray))
                df_gain[str(gain_value)] = yarray
            filename = str(temperature) + '_' + str(Integration) + '_' + 'gain.csv'
            df_gain.to_csv(filename, index=False)
            df_std_g = pd.DataFrame({'Gain': global_variables.gain_array, 'STD': std_array})
            optimized_gain = find_optimized_gain(df_std_g)
            _type.append('G')
            _temperature.append(temperature)
            _integration.append(Integration)
            _gain.append(optimized_gain[2])
            _offset.append(optimized_offset[2])
            _std.append(optimized_gain[3])
    df3 = pd.DataFrame({'Type': _type,
                        'Temperature': _temperature,
                        'Integration time(s)': _integration,
                        'Optimized Gain': _gain,
                        'Optimized offset': _offset,
                        'Standard deviation': _std})
    df3.to_csv('CDCalibration.csv', index=False)
    label_CDC['text'] = 'Done'

    # figure2 = Figure(figsize=(8, 4), dpi=100)
    # display2 = figure2.add_subplot()
    # display2.set_title(f'STD curve @ temperature {temperature} : integration time {Integration}')
    # display2.set_xlabel('Offset')
    # display2.set_ylabel('Standard deviation')
    # canvas = FigureCanvasTkAgg(figure2, master=root)
    # canvas.get_tk_widget().place(x=600, y=800)
    # display2.plot(global_variables.offset_array, std_array)
    # label_CDC['text'] = f'Optimized offset is {optimized_offset[2]}'
    # figure3 = Figure(figsize=(8, 4), dpi=100)
    # display3 = figure3.add_subplot()
    # display3.set_title(f'STD curve @ temperature {temperature} : integration time {Integration}')
    # display3.set_xlabel('Gain')
    # display3.set_ylabel('Standard deviation')
    # canvas = FigureCanvasTkAgg(figure3, master=root)
    # canvas.get_tk_widget().place(x=300, y=450)
    # display3.plot(gain_array, std_array)


def close():
    isUSBClosed = add_lib.bwtekCloseUSB(global_variables.Channel)
    if isUSBClosed:
        label_test['text'] = 'Device is closed'
        button_inttime['state'] = 'disabled'
        button_scan['state'] = 'disabled'
        button_GetInGaAsMode['state'] = 'disabled'
        button_SetInGaAsMode['state'] = 'disabled'
        button_readTemperature1['state'] = 'disabled'
        button_readTemperature2['state'] = 'disabled'
        button_setTemperature1['state'] = 'disabled'
        button_setTemperature2['state'] = 'disabled'
        button_setGain_Offset['state'] = 'disabled'
        button_scan['state'] = 'disabled'
        button_CDC['state'] = 'disabled'


root = tk.Tk()
root.title('SpectroTest')
root.geometry('1200x900+50+50')
root.resizable(True, True)

tabControl = ttk.Notebook(root)
tab_functions = ttk.Frame(tabControl)
tab_acquisition = ttk.Frame(tabControl)
tab_cdc = ttk.Frame(tabControl)
tab_temperature = ttk.Frame(tabControl)
tab_laser = ttk.Frame(tabControl)
tab_monitoring = ttk.Frame(tabControl)
tabControl.add(tab_functions, text=' Functions Test ')
tabControl.add(tab_acquisition, text='Acquisition')
tabControl.add(tab_cdc, text=' Channel Difference Calibration ')
tabControl.add(tab_laser, text=' Laser ')
tabControl.add(tab_monitoring, text=' Monitoring ')
tabControl.pack(expand=1, fill="both")

interfacetype = tk.StringVar()
radio_interface_USB = ttk.Radiobutton(tab_functions, text='USB', variable=interfacetype, value=1,
                                      command=setInterface)
radio_interface_RS232 = ttk.Radiobutton(tab_functions, text='RS232', variable=interfacetype, value=2,
                                        command=setInterface)
radio_interface_OTHERS = ttk.Radiobutton(tab_functions, text='Others', variable=interfacetype, value=3,
                                         command=setInterface)
radio_interface_USB.place(x=250, y=10)
radio_interface_RS232.place(x=350, y=10)
radio_interface_OTHERS.place(x=450, y=10)

label_comPort = ttk.Label(tab_functions, text='COM port')
comPort = tk.StringVar()
textbox_comport = ttk.Entry(tab_functions, textvariable=comPort, width=10)
textbox_comport.insert(0, str(3))

button_initialize = ttk.Button(tab_functions, text='Initialize spectrometer', state='disabled', width=30,
                               command=initialization)
button_initialize.place(x=10, y=40)

button_readEEPROM = ttk.Button(tab_functions, text='Read EEPROM', state='disabled', width=30, command=readEEPROM)
button_readEEPROM.place(x=10, y=70)

label_test = ttk.Label(tab_functions, text='')
button_Test = ttk.Button(tab_functions, text='Test', state='disabled', width=30, command=test)
button_Test.place(x=10, y=100)

button_GetInGaAsMode = ttk.Button(tab_functions, text='Get InGaAs mode', state='disabled', width=30,
                                  command=getInGaAsMode)
button_GetInGaAsMode.place(x=10, y=130)

button_SetInGaAsMode = ttk.Button(tab_functions, text='Set InGaAs mode', state='disabled', width=30,
                                  command=setInGaAsMode)
button_SetInGaAsMode.place(x=10, y=160)

InGaAs = tk.StringVar(value=global_variables.InGaAsMode)
listbox_IGA = tk.Listbox(tab_functions, listvariable=InGaAs, height=2, selectmode='browse')
listbox_IGA.bind('<<ListboxSelect>>', setIGAValue)

button_readTemperature1 = ttk.Button(tab_functions, text='Read detector temperature', state='disabled', width=30,
                                     command=getTemperature_stage1)
button_readTemperature1.place(x=10, y=190)

button_readTemperature2 = ttk.Button(tab_functions, text='Read chamber temperature', state='disabled', width=30,
                                     command=getTemperature_stage2)
button_readTemperature2.place(x=10, y=220)

button_setTemperature1 = ttk.Button(tab_functions, text='Set detector temperature', state='disabled', width=30,
                                    command=setTemperature_stage1)
button_setTemperature1.place(x=10, y=250)

label_setDetectorT = ttk.Label(tab_functions, text='Detector T (-25 to 0)')
setDetectorT = tk.StringVar()
textbox_setDetectorTemp = ttk.Entry(tab_functions, textvariable=setDetectorT, width=10)
textbox_setDetectorTemp.insert(0, '-25')

button_setTemperature2 = ttk.Button(tab_functions, text='Set chamber temperature', state='disabled', width=30,
                                    command=setTemperature_stage2)
button_setTemperature2.place(x=10, y=280)

label_setChamberT = ttk.Label(tab_functions, text='Chamber T (10 to 30)')
setChamberT = tk.StringVar()
textbox_setChamberTemp = ttk.Entry(tab_functions, textvariable=setChamberT, width=10)
textbox_setChamberTemp.insert(0, '20')

label_gain = ttk.Label(tab_functions, text='Gain (0-65535)')
gaintext = tk.StringVar()
textbox_gain = ttk.Entry(tab_functions, textvariable=gaintext, width=10)

label_offset = ttk.Label(tab_functions, text='Offset (0-4095)')
offsettext = tk.StringVar()
textbox_offset = ttk.Entry(tab_functions, textvariable=offsettext, width=10)
# textbox_offset.insert(0, str(offset))

button_readGain_Offset = ttk.Button(tab_functions, text='Read Gain and Offset', state='disabled', width=30,
                                    command=getGainOffset)
button_readGain_Offset.place(x=10, y=310)

button_setGain_Offset = ttk.Button(tab_functions, text='Set Gain and Offset', state='disabled', width=30,
                                   command=setGainOffset)
button_setGain_Offset.place(x=10, y=340)

label_inttime = ttk.Label(tab_functions, text='Integration time (ms)')
inttimetext = tk.StringVar()
textbox_inttime = ttk.Entry(tab_functions, textvariable=inttimetext, width=10)
textbox_inttime.insert(0, '1000')
button_inttime = ttk.Button(tab_functions, text="Set Integration time", state='disabled', width=30,
                            command=setIntegrationTime)
button_inttime.place(x=10, y=370)

button_scan = ttk.Button(tab_functions, text='Scan', state='disabled', width=30,
                         command=scan)
button_scan.place(x=10, y=400)

button_multiscan = ttk.Button(tab_functions, text='Multi-Scan', state='disabled', width=30,
                              command=multiscan)
button_multiscan.place(x=10, y=430)

button_monitor = ttk.Button(tab_functions, text='Monitoring', state='disabled', width=30, command=monitor)
button_monitor.place(x=10, y=460)
Enable_tempmonitor = tk.IntVar()
check_temperature = ttk.Checkbutton(tab_functions,
                                    text='Temperature monitoring',
                                    variable=Enable_tempmonitor,
                                    onvalue=1,
                                    offvalue=0)
Enable_tempmonitor.set(0)
check_temperature.place(x=220, y=460)
label_totalscan = ttk.Label(tab_functions, text=' # of Total scans:')
label_totalscan.place(x=10, y=490)
num_totalscan = tk.StringVar()
textbox_totalscan = ttk.Entry(tab_functions, textvariable=num_totalscan, width=10)
textbox_totalscan.insert(0, '10')
textbox_totalscan.place(x=120, y=490)

button_writeEEPROM = ttk.Button(tab_functions, text='Write EEPROM', state='disabled', width=30, command=writeEEPROM)
button_writeEEPROM.place(x=10, y=520)

button_close = ttk.Button(tab_functions, text='Close device', state='disabled', width=30,
                          command=close)
button_close.place(x=10, y=550)

# Acquisition
label_inttime_concate1 = ttk.Label(tab_acquisition, text='Integration time (ms)')
label_inttime_concate1.place(x=10, y=10)
inttimetext_concate1 = tk.StringVar()
textbox_inttime_concate1 = ttk.Entry(tab_acquisition, textvariable=inttimetext_concate1, width=10)
textbox_inttime_concate1.insert(0, '1000')
textbox_inttime_concate1.place(x=150, y=10)
button_inttime_concate1 = ttk.Button(tab_acquisition, text='Set', state='disabled', width=5,
                                     command=setIntegrationTime)
button_inttime_concate1.place(x=250, y=10)

label_inttime_concate2 = ttk.Label(tab_acquisition, text='Integration time (ms)')

inttimetext_concate2 = tk.StringVar()
textbox_inttime_concate2 = ttk.Entry(tab_acquisition, textvariable=inttimetext_concate2, width=10)
textbox_inttime_concate2.insert(0, '1000')

button_inttime_concate2 = ttk.Button(tab_acquisition, text='Set', state='disabled', width=5,
                                     command=setIntegrationTime)
####
laseroption2 = tk.IntVar()
radio_laser_02 = ttk.Radiobutton(tab_acquisition, text='No Laser selected', variable=laseroption2, value=0,
                                 command=Config_Laser)
radio_laser_12 = ttk.Radiobutton(tab_acquisition, text='Single Laser', variable=laseroption2, value=1,
                                 command=Config_Laser)
radio_laser_22 = ttk.Radiobutton(tab_acquisition, text='Dual Lasers', variable=laseroption2, value=2,
                                 command=Config_Laser)
laseroption2.set(0)

radio_laser_02.place(x=10, y=70)
radio_laser_12.place(x=150, y=70)
radio_laser_22.place(x=250, y=70)

label_laser1 = ttk.Label(tab_acquisition)
label_laser2 = ttk.Label(tab_acquisition)

LP2a = tk.StringVar()
textbox_laserpower2a = ttk.Entry(tab_acquisition, textvariable=LP2a, width=10)
textbox_laserpower2a.insert(0, '100.0')

LP2b = tk.StringVar()
textbox_laserpower2b = ttk.Entry(tab_acquisition, textvariable=LP2b, width=10)
textbox_laserpower2b.insert(0, '100.0')

button_scan2 = ttk.Button(tab_acquisition, text='Scan 2', state='disabled', width=30, command=scan2)
button_scan2.place(x=10, y=430)

xaxistype = tk.IntVar()
radio_xaxistype_0 = ttk.Radiobutton(tab_acquisition, text='pixel', variable=xaxistype, value=0,
                                    command=SP_plot)
radio_xaxistype_1 = ttk.Radiobutton(tab_acquisition, text='wavelength', variable=xaxistype, value=1,
                                    command=SP_plot)
radio_xaxistype_2 = ttk.Radiobutton(tab_acquisition, text='Raman Shift', variable=xaxistype, value=2,
                                    command=SP_plot)
radio_xaxistype_3 = ttk.Radiobutton(tab_acquisition, text='Interp Raman Shift', variable=xaxistype, value=3,
                                    command=SP_plot)

xaxistype.set(0)
radio_xaxistype_0.place(x=30, y=460)
radio_xaxistype_1.place(x=30, y=490)
radio_xaxistype_2.place(x=30, y=520)
radio_xaxistype_3.place(x=30, y=550)

show_concat = tk.IntVar()
check_showconcat = ttk.Checkbutton(tab_acquisition,
                                   text='Show concatenation',
                                   variable=show_concat,
                                   onvalue=1,
                                   offvalue=0)
show_concat.set(0)

label_concat = ttk.Label(tab_acquisition, text='Concatenating at (cm-1) ')
ConcatP = tk.StringVar()
textbox_concat = ttk.Entry(tab_acquisition, textvariable=ConcatP, width=10)
textbox_concat.insert(0, '2000')

Enable_dark = tk.IntVar()
check_dark = ttk.Checkbutton(tab_acquisition,
                             text='Auto Dark',
                             variable=Enable_dark,
                             onvalue=1,
                             offvalue=0)
Enable_dark.set(0)
check_dark.place(x=30, y=640)

# Laser
button_initializeLaser = ttk.Button(tab_laser, text='Initialize laser', width=30, command=initializeLaser)
button_initializeLaser.place(x=10, y=10)

label_initializeLaser = ttk.Label(tab_laser, width=30, text='laser to be initialized')
label_initializeLaser.place(x=250, y=10)

laseroption = tk.IntVar()
radio_laser_0 = ttk.Radiobutton(tab_laser, text='No Laser selected', variable=laseroption, value=0,
                                command=SetLaser)
radio_laser_1 = ttk.Radiobutton(tab_laser, text='Laser 1', variable=laseroption, value=1,
                                command=SetLaser)
radio_laser_2 = ttk.Radiobutton(tab_laser, text='Laser 2', variable=laseroption, value=2,
                                command=SetLaser)
label_getIPSLaserAddress = ttk.Label(tab_laser)
label_getIPSLaserModelname = ttk.Label(tab_laser)
label_getIPSLaserSN = ttk.Label(tab_laser)
label_getIPSLaserLEW = ttk.Label(tab_laser)
label_getIPSLaserenable = ttk.Label(tab_laser)
label_getIPSLaserPWMEnable = ttk.Label(tab_laser)
label_getIPSLaserPWMDuty = ttk.Label(tab_laser)
label_getIPSLaserBoardTemp = ttk.Label(tab_laser)
label_getIPSLaserBoardCurrent = ttk.Label(tab_laser)
label_getIPSLaserBoardStatus = ttk.Label(tab_laser)
label_getIPSLaserPower = ttk.Label(tab_laser)
label_getIPSLaserCurrent = ttk.Label(tab_laser)
label_getIPSLaserTECTemp = ttk.Label(tab_laser)

button_setLP = ttk.Button(tab_laser, text='Set Laser Power', state='disabled', width=30,
                          command=setLaserPower)
button_setLP.place(x=10, y=460)

label_laserpower = ttk.Label(tab_laser, text='0-100%')
label_laserpower.place(x=250, y=460)
LP = tk.StringVar()
textbox_laserpower = ttk.Entry(tab_laser, textvariable=LP, width=10)
textbox_laserpower.insert(0, '100.0')
textbox_laserpower.place(x=350, y=460)

button_closeLaser = ttk.Button(tab_laser, text='Close Laser', width=30, command=closeLaser)
button_closeLaser.place(x=10, y=490)

#

# Channel difference calibration session
button_CDC = ttk.Button(tab_cdc, text='Channel Difference Calibration', state='disabled', width=30,
                        command=CDC)
button_CDC.place(x=10, y=10)
label_CDC = ttk.Label(tab_cdc)
label_CDC.place(x=250, y=10)

root.mainloop()
