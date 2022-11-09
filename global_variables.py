from ctypes import *
import numpy as np

baudrate = 115200
comport = 0
SpectrometerType = 94
Model = ''
PixelNum = 2048
TimingMode = c_int(1)
InputMode = c_int(2)
Param = c_int(0)
a_coff = [0, 0, 0, 0]
LEW = 785
LEW2 = 785

ReverseX = 0
ReverseY = 0

# InGaAs mode
InGaAsMode = ('High Sensitivity', 'High Dynamic')
getModeValue = c_int(0)
setModelValue = c_int(0)

# Temperature
Command1 = c_int(0x41)    # read
Command2 = c_int(0x42)
ADValue = c_int(0)
DAChannel1 = 0       # write
DAChannel2 = 1
nMuxOut = 0

setTemperature1 = -20
setTemperature2 = 30
getTemperature1 = c_double(-10)
getTemperature2 = c_double(20)

# gain and offset
gain = 10000
offset = 1000
pin_set_gain = 5
pin_set_offset = 4

integration_time = 1000
integration_time2 = 1000
time_factor = 1
laser_power = c_double(0.0)    # percentage
laser_power2 = c_double(0.0)
trigger = c_int(0)
Channel = c_int(0)

detector_temperature_array = [-25]
chamber_temperature_array = [20]
integration_time_array = [1000, 5000, 10000, 30000, 60000]

gain_array = np.arange(10000, 60001, 1000)
offset_array = np.arange(100, 4001, 100)

LaserType = 0
LaserTypes = ['None', 'Cleanlaze', 'IPS', 'HH laser']
IPSLaser1 = 0x14  # 860
IPSLaser2 = 0x15  # 1064
LR_channel = 0
IPSModel = ''
IPSSN = ''
IPSWL = ''
IPSVersion = ''
IPSLaserAdd = 0x15


InterfaceType = 0
InterfaceTypes = ['USB', 'RS232', 'OTHERS']

modelwith2stagecooling = ['BTC284N', 'BTC281Y', 'HHEX', 'BTC284C']
modelwithCDC = ['BTC284N', 'BTC281Y', 'HHEX']

pixel_array = []
data_P_array = []
Wavelength_array = []
data_W_array = []
Wavelength_array_interp = []
data_W_array_interp = []
RamanShift_array = []
data_RS_array = []
RamanShift_array_interp = []
data_RS_array_interp = []

pixel_array2 = []
data_P_array2 = []
Wavelength_array2 = []
data_W_array2 = []
Wavelength_array_interp2 = []
data_W_array_interp2 = []
RamanShift_array2 = []
data_RS_array2 = []
RamanShift_array_interp2 = []
data_RS_array_interp2 = []

RamanShift_array_concat = []
data_RS_array_concat = []

dark_array = []

