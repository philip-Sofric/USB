def parse_line(str_array):
    para = ''
    start = 0
    for character in str_array:
        if character == '=':
            start = 1
        else:
            if start == 0:
                continue
            elif character == '-':
                break
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

