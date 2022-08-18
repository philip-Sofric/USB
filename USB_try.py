import libusb as usb
import ctypes as ct



usb.init(None)
devs = ct.POINTER(ct.POINTER(usb.device))()
cnt = usb.get_device_list(None, ct.byref(devs))

for i in range(cnt):
    desc = usb.device_descriptor()
    ret = usb.get_device_descriptor(devs[i], ct.byref(desc))
    if ret < 0:
        print("failed to get device descriptor")
    print("Dev (bus {}, device {}): {:04X} - {:04X} speed: {}".format(
        usb.get_bus_number(devs[i]), usb.get_device_address(devs[i]),
        desc.idVendor, desc.idProduct, usb.get_device_speed(devs[i])))
hd = usb.open_device_with_vid_pid(None, ct.c_uint16(0x0781), ct.c_uint16(0x55A9))
print(hd)
add_handle = ct.pointer(hd)
print(add_handle)
interface = usb.claim_interface(hd, 0)
# print(interface)

# dev = usb.get_device(hd)
# desc = usb.device_descriptor()
# ret = usb.get_device_descriptor(hd, ct.byref(desc))
# print("Dev (bus {}, device {}): {:04X} - {:04X} speed: {}".format(
#         usb.get_bus_number(hd), usb.get_device_address(hd),
#         desc.idVendor, desc.idProduct, usb.get_device_speed(hd)))
# desc_ =
# print('vid is ', usb)
usb.close(hd)
# usb.free_device_list(devs, 1)
usb.exit(None)
