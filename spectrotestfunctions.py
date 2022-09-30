from scipy.signal import savgol_filter as sg_smoothing
import numpy as np
import pandas as pd
from scipy import interpolate


def parse_line(str_array):
    para = ''
    start = 0
    for character in str_array:
        if character == '=':
            start = 1
        else:
            if start == 0:
                continue
            # elif character == '-':
            #     break
            else:
                para += character
    return para


def getPixelNumfromEEPROM(parafilename):
    _PixelNum = 0
    with open(parafilename) as file:
        for line in map(str.strip, file):
            if line.startswith('pixel_num'):
                _PixelNum = int(parse_line(line))
                break
    return _PixelNum


def getModelfromEEPROM(parafilename):
    _Model = 0
    with open(parafilename) as file:
        for line in map(str.strip, file):
            if line.startswith('model'):
                _Model = str(parse_line(line))
                if _Model.startswith('BTC284N'):
                    _Model = 'BTC284N'
                elif _Model.startswith('BWS492') or _Model.startswith('BWS493'):
                    _Model = 'HHEX'
                break
    return _Model


def getSPTypefromEEPROM(parafilename):
    _SpectrometerType = 0
    with open(parafilename) as file:
        for line in map(str.strip, file):
            if line.startswith('spectrometer_type'):
                _SpectrometerType = int(parse_line(line))
                break
    return _SpectrometerType


def getTimingModefromEEPROM(parafilename):
    _TimingMode = 0
    with open(parafilename) as file:
        for line in map(str.strip, file):
            if line.startswith('timing_mode'):
                _TimingMode = int(parse_line(line))
                break
    return _TimingMode


def getInputModefromEEPROM(parafilename):
    _InputMode = 0
    with open(parafilename) as file:
        for line in map(str.strip, file):
            if line.startswith('input_mode'):
                _InputMode = int(parse_line(line))
                break
    return _InputMode


def geta_coeffromEEPROM(parafilename):
    _a_coeff = np.zeros(4)
    with open(parafilename) as file:
        for line in map(str.strip, file):
            if line.startswith('coefs_a0'):
                _a_coeff[0] = float(parse_line(line))
            if line.startswith('coefs_a1'):
                _a_coeff[1] = float(parse_line(line))
            if line.startswith('coefs_a2'):
                _a_coeff[2] = float(parse_line(line))
            if line.startswith('coefs_a3'):
                _a_coeff[3] = float(parse_line(line))
    return _a_coeff


def getLaserwavelengthfromEEPROM(parafilename):
    _LEW = 0
    with open(parafilename) as file:
        for line in map(str.strip, file):
            if line.startswith('laser_wavelength'):
                _LEW = float(parse_line(line))
    return _LEW


def getGainfromEEPROM(parafilename):
    _gain = 0
    with open(parafilename) as file:
        for line in map(str.strip, file):
            if line.startswith('OPAM_Gain'):
                _gain = int(parse_line(line))
    return _gain


def getOffsetfromEEPROM(parafilename):
    _offset = 0
    with open(parafilename) as file:
        for line in map(str.strip, file):
            if line.startswith('VideoSignal_Offset'):
                _offset = int(parse_line(line))
    return _offset


def getReversefromEEPROM(parafilename):
    _ReverseX = 0
    _ReverseY = 0
    with open(parafilename) as file:
        for line in map(str.strip, file):
            if line.startswith('xaxis_data_reverse'):
                _ReverseX = int(parse_line(line))
            elif line.startswith('yaxis_data_reverse'):
                _ReverseY = int(parse_line(line))
    return _ReverseX, _ReverseY


def calc_STD(ydata):
    y_SGSmooth = sg_smoothing(ydata, 99, 3)
    y_Straighten = ydata - y_SGSmooth
    STD_straighten = y_Straighten.std()
    return STD_straighten


def find_optimized_offset(datafile):
    offset_column = datafile['Offset']
    std_column = datafile['STD']
    offset_interp_column = np.arange(100, 4001, 1)
    tck = interpolate.splrep(offset_column, std_column, s=0)
    std_interp_column = interpolate.splev(offset_interp_column, tck, der=0)
    df_1 = pd.DataFrame({'offset_column': offset_column,
                         'STD column': std_column})
    df_2 = pd.DataFrame({'Offset_interp': offset_interp_column,
                         'STD_interp': std_interp_column})
    min_values = find_minimum(df_1)
    min_values_interp = find_minimum(df_2)
    data_return = [min_values[0], min_values[1], min_values_interp[0], min_values_interp[1]]
    return data_return


def find_optimized_gain(datafile):
    gain_column = datafile['Gain']
    std_column = datafile['STD']
    gain_interp_column = np.arange(10000, 50001, 100)
    tck = interpolate.splrep(gain_column, std_column, s=0)
    std_interp_column = interpolate.splev(gain_interp_column, tck, der=0)
    df_1 = pd.DataFrame({'Gain_column': gain_column,
                         'STD column': std_column})
    df_2 = pd.DataFrame({'Gain_interp': gain_interp_column,
                         'STD_interp': std_interp_column})
    min_values = find_minimum(df_1)
    min_values_interp = find_minimum(df_2)
    data_return = [min_values[0], min_values[1], min_values_interp[0], min_values_interp[1]]
    return data_return


def find_minimum(datafile):
    column_0 = datafile.iloc[:, 0]
    column_1 = datafile.iloc[:, 1]
    row_number = len(column_0)
    row_number_array = np.arange(0, row_number, 1)
    min_values = []
    for k in row_number_array:
        if column_1[k] == min(column_1):
            min_values.append(column_0[k])
            min_values.append(column_1[k])
            break
    return min_values


def convertASCII2string(pointerarray, leng):
    name_string = ''
    for i in np.arange(0, leng, 1):
        if pointerarray[i] != 0:
            name_string += chr(pointerarray[i])
        else:
            break
    return name_string
