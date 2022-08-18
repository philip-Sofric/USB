import usb.core

device = usb.core.find(idVendor=0x0781, idProduct=0x55A9)
print(device.bLength)
device.set_configuration()