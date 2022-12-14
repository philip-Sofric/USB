# Functions in response to events from interface

from spectrotest import *
import global_variables
from ctypes import *
from SDKfunctions import *


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
    global_variables.a_coff = geta_coeffromEEPROM('p')
    global_variables.ReverseX, global_variables.ReverseY = getReversefromEEPROM(parafile)
    # parameters by SP model
    if global_variables.Model == 'BTC284N':
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
    print(f'Interface type is {global_variables.InterfaceTypes[global_variables.InterfaceType]}')
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
    else:
        label_initialize['text'] = 'device initialization fails'
        button_readEEPROM['state'] = 'disabled'


def readEEPROM():
    label_EEPROM = ttk.Label(tab_functions)
    label_EEPROM.place(x=250, y=70)
    if SP_EEPROM() > 0:
        param_config('p')
        # print('Model is', global_variables.Model)
        label_EEPROM.config(text=f'EEPROM reading is successful. Model is {global_variables.Model}')
        # Operations on Tkinter widgets
        button_Test['state'] = 'normal'
        textbox_gain.insert(0, str(global_variables.gain))
        textbox_offset.insert(0, str(global_variables.offset))

        #
        # reference info print screen
        print('X reverse is {}, Y reserve is {}'.format(global_variables.ReverseX, global_variables.ReverseY))
        #
    else:
        button_Test['state'] = 'disabled'
        label_EEPROM['text'] = 'EEPROM reading fails'


def test():
    label_test.place(x=250, y=100)
    if SP_test() > 0:
        label_test['text'] = 'Device is ready'
        button_inttime['state'] = 'normal'
        label_inttime.place(x=220, y=370)
        textbox_inttime.place(x=350, y=370)
        button_scan['state'] = 'normal'
        button_close['state'] = 'normal'
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


def setIGAValue(event):
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
    if t > 0 and global_variables.LaserType == 1:
        radio_laser_0.place(x=50, y=40)
        radio_laser_1.place(x=200, y=40)
        radio_laser_2.place_forget()

    elif t > 0 and global_variables.LaserType == 2:
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
        button_setLP['state'] = 'disabled'
        label_getIPSLaserAddress.place_forget()
        label_getIPSLaserLEW.place_forget()
        label_getIPSLaserPWMDuty.place_forget()
        label_getIPSLaserPower.place_forget()
    elif global_variables.LaserType == 1:
        pass  # Cleanlaze
    elif global_variables.LaserType == 2:
        if lo == 1:
            global_variables.IPSLaserAdd = 20
        elif lo == 2:
            global_variables.IPSLaserAdd = 21
        else:
            pass
        button_setLP['state'] = 'normal'
        print('This is to check which laser is selected', global_variables.IPSLaserAdd)

        Set_Laser(global_variables.IPSLaserAdd)
        Get_All_LaserInfo(global_variables.IPSLaserAdd)
        # add_lib.bwtekSetIPSLaserFactorySetting2PowerUpSetting(0)
        label_getIPSLaserAddress['text'] = global_variables.IPSLaserAdd
        label_getIPSLaserLEW['text'] = str(global_variables.IPSWL)

        print(global_variables.IPSWL)
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
    elif global_variables.LaserType == 3:
        pass  # hh laser


def Config_Laser():
    pass


def getLaserWL():
    pass


def setLaserPower():
    global_variables.laser_power.value = float(LP.get())
    print('Laser power to be set is ', global_variables.laser_power.value)
    Set_Laser_Power(global_variables.laser_power)


def closeLaser():
    Close_Laser()


def scan():
    # print(time_factor)
    # print(('Model is ', Model))
    xarray = np.arange(0, global_variables.PixelNum, 1)
    data_array = (c_ushort * global_variables.PixelNum)()
    figure = Figure(figsize=(6, 3), dpi=100)
    display = figure.add_subplot()
    display.set_title('Spectrum')
    display.set_xlabel('Pixel')
    display.set_ylabel('Intensity')
    display.set_xlim(0, 600)
    display.set_ylim(0, 65535)
    canvas = FigureCanvasTkAgg(figure, master=root)
    canvas.get_tk_widget().place(x=650, y=250)
    DT = []

    isDataReadSuccessful = -1
    if global_variables.InterfaceType == 0:
        isDataReadSuccessful = add_lib.bwtekDataReadUSB(global_variables.trigger, byref(data_array),
                                                        global_variables.Channel)
    elif global_variables.InterfaceType == 1:
        a = time.time()
        isDataReadSuccessful = add_librs.bwtekDataReadRS232(global_variables.trigger, byref(data_array),
                                                            global_variables.Channel)
        b = time.time()
        print(f'delta time is {(b - a):6.4} s')
    if isDataReadSuccessful == global_variables.PixelNum:
        if global_variables.ReverseX == 1:
            xarray = xarray[::-1]
        for j in range(global_variables.PixelNum):
            if global_variables.ReverseY == 1:
                DT.append(65535 - data_array[j])
            else:
                DT.append(data_array[j])
        DT = np.array(DT)
        display.plot(xarray, DT)
        canvas.draw()

    else:
        print('scan fails')
    return xarray, DT


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
    for temperature in global_variables.detector_temperature_array:
        temp_set_count = 0
        add_lib.bwtekReadTemperature(global_variables.Command1, byref(global_variables.ADValue),
                                     byref(global_variables.getTemperature1), global_variables.Channel)
        label_CDC['text'] = f'Initial detector temperature is {global_variables.getTemperature1.value:6.4}'
        # detector temperature stabilization
        while abs(global_variables.getTemperature1.value - temperature) > 1.0 and temp_set_count <= 20:
            add_lib.bwtekSetTemperatureUSB(global_variables.DAChannel1, temperature, global_variables.Channel)
            temp_set_count += 1
            # time.sleep(2)
            add_lib.bwtekReadTemperature(global_variables.Command1, byref(global_variables.ADValue),
                                         byref(global_variables.getTemperature1), global_variables.Channel)
        if temp_set_count > 20:
            label_CDC[
                'text'] = f'Detector cannot be stabilized. Current temperature is {global_variables.getTemperature1.value}'
        else:
            label_CDC['text'] = f'Stabilized temperature is {global_variables.getTemperature1.value}...\n'
        # no matter temperature is stabilized or not, calibration continues...
        # abandon the first data right after temperature change
        add_lib.bwtekSetTimeUSB(200, global_variables.Channel)
        label_CDC['text'] = 'Scanning'
        xarray, yarray = scan()
        label_CDC['text'] = 'First scan after temp change is abandoned'
        for Integration in global_variables.integration_time_array:
            add_lib.bwtekSetTimeUSB(Integration * 100, global_variables.Channel)
            # begin for offset calibration. Offset scans with laser off, set gain as 40000
            std_array = []
            df = pd.DataFrame({'Pixel': xarray})
            gain_value = 40000
            add_lib.bwtekSetAnalogOut(5, gain_value, global_variables.Channel)
            for offset_value in global_variables.offset_array:
                add_lib.bwtekSetAnalogOut(4, int(offset_value), global_variables.Channel)
                label_CDC[
                    'text'] = f'Scanning: temp {temperature}, time {Integration}, gain {gain_value}, offset {offset_value}'
                xarray, yarray = scan()
                std_array.append(calc_STD(yarray))
                df[str(offset_value)] = yarray
            filename = str(temperature) + '_' + str(Integration) + '_' + 'offset.csv'
            df.to_csv(filename, index=False)
            figure2 = Figure(figsize=(8, 4), dpi=100)
            display2 = figure2.add_subplot()
            display2.set_title(f'STD curve @ temperature {temperature} : integration time {Integration}')
            display2.set_xlabel('Offset')
            display2.set_ylabel('Standard deviation')
            canvas = FigureCanvasTkAgg(figure2, master=root)
            canvas.get_tk_widget().place(x=600, y=800)
            display2.plot(global_variables.offset_array, std_array)
            df2 = pd.DataFrame({'Offset': global_variables.offset_array, 'STD': std_array})
            optimized_offset = find_optimized_offset(df2)
            label_CDC['text'] = f'Optimized offset is {optimized_offset[2]}'

            _type.append('O')
            _temperature.append(temperature)
            _integration.append(Integration)
            _gain.append(40000)
            _offset.append(optimized_offset[2])
            _std.append(optimized_offset[3])
            # end for offset calibration
            # # begin for gain calibration. gain scans with laser on, set optimized offset obtained above
            # std_array = []
            # df = pd.DataFrame({'Pixel': xarray})
            # offset_value = optimized_offset[2]
            # add_lib.bwtekSetAnalogOut(4, offset_value, Channel)
            # for gain_value in gain_array:
            #     add_lib.bwtekSetAnalogOut(5, int(gain_value), Channel)
            #     label_CDC[
            #         'text'] = f'Scanning: temp {temperature}, time {Integration}, gain {gain_value}, offset {offset_value} '
            #     xarray, yarray = scan()
            #     std_array.append(calc_STD(yarray))
            #     df[str(gain_value)] = yarray
            # filename = str(temperature) + '_' + str(Integration) + '_' + 'gain.csv'
            # df.to_csv(filename, index=False)
            # figure3 = Figure(figsize=(8, 4), dpi=100)
            # display3 = figure3.add_subplot()
            # display3.set_title(f'STD curve @ temperature {temperature} : integration time {Integration}')
            # display3.set_xlabel('Gain')
            # display3.set_ylabel('Standard deviation')
            # canvas = FigureCanvasTkAgg(figure3, master=root)
            # canvas.get_tk_widget().place(x=300, y=450)
            # display3.plot(gain_array, std_array)
            # df2 = pd.DataFrame({'Gain': gain_array, 'STD': std_array})
            # optimized_gain = find_optimized_offset(df2)
            # label_CDC['text'] = f'Optimized gain is {optimized_gain[2]} @ offset {offset_value}'
            #
            # _type.append('G')
            # _temperature.append(temperature)
            # _integration.append(Integration)
            # _gain.append(optimized_gain[2])
            # _offset.append(optimized_offset[2])
            # _std.append(optimized_gain[3])
            # # end for gain calibration
    df3 = pd.DataFrame({'Type': _type,
                        'Temperature': _temperature,
                        'Integration time(s)': _integration,
                        'Optimized Gain': _gain,
                        'Optimized offset': _offset,
                        'Standard deviation': _std})
    df3.to_csv('CDCalibration.csv', index=False)
    label_CDC['text'] = 'Done'


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
