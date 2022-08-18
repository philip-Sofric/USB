import ctypes as ct
import libusb as usb
import sys
import os
# from libusb._platform import is_linux

verbose = False


def print_endpoint_comp(ep_comp):
    print("      USB 3.0 Endpoint Companion:")
    print("        bMaxBurst:           {:d}".format(ep_comp.bMaxBurst))
    print("        bmAttributes:        {:02x}h".format(ep_comp.bmAttributes))
    print("        wBytesPerInterval:   {:d}".format(ep_comp.wBytesPerInterval))


def print_endpoint(endpoint):
    print("      Endpoint:")
    print("        bEndpointAddress:    {:02x}h".format(endpoint.bEndpointAddress))
    print("        bmAttributes:        {:02x}h".format(endpoint.bmAttributes))
    print("        wMaxPacketSize:      {:d}".format(endpoint.wMaxPacketSize))
    print("        bInterval:           {:d}".format(endpoint.bInterval))
    print("        bRefresh:            {:d}".format(endpoint.bRefresh))
    print("        bSynchAddress:       {:d}".format(endpoint.bSynchAddress))
    i = 0
    while i < endpoint.extra_length:
        if endpoint.extra[i + 1] == usb.LIBUSB_DT_SS_ENDPOINT_COMPANION:
            ep_comp = ct.POINTER(usb.ss_endpoint_companion_descriptor)()
            ret = usb.get_ss_endpoint_companion_descriptor(None, ct.byref(endpoint),
                                                           ct.byref(ep_comp))
            if ret != usb.LIBUSB_SUCCESS:
                continue
            print_endpoint_comp(ep_comp[0])
            usb.free_ss_endpoint_companion_descriptor(ep_comp)
        i += endpoint.extra[i]


def print_altsetting(interface):
    print("    Interface:")
    print("      bInterfaceNumber:      {:d}".format(interface.bInterfaceNumber))
    print("      bAlternateSetting:     {:d}".format(interface.bAlternateSetting))
    print("      bNumEndpoints:         {:d}".format(interface.bNumEndpoints))
    print("      bInterfaceClass:       {:d}".format(interface.bInterfaceClass))
    print("      bInterfaceSubClass:    {:d}".format(interface.bInterfaceSubClass))
    print("      bInterfaceProtocol:    {:d}".format(interface.bInterfaceProtocol))
    print("      iInterface:            {:d}".format(interface.iInterface))
    for i in range(interface.bNumEndpoints):
        print_endpoint(interface.endpoint[i])


def print_2_0_ext_cap(usb_2_0_ext_cap):
    print("    USB 2.0 Extension Capabilities:")
    print("      bDevCapabilityType:    {:d}".format(usb_2_0_ext_cap.bDevCapabilityType))
    print("      bmAttributes:          {:08x}h".format(usb_2_0_ext_cap.bmAttributes))


def print_ss_usb_cap(ss_usb_cap: usb.ss_usb_device_capability_descriptor):
    print("    USB 3.0 Capabilities:")
    print("      bDevCapabilityType:    {:d}".format(ss_usb_cap.bDevCapabilityType))
    print("      bmAttributes:          {:02x}h".format(ss_usb_cap.bmAttributes))
    print("      wSpeedSupported:       {:d}".format(ss_usb_cap.wSpeedSupported))
    print("      bFunctionalitySupport: {:d}".format(ss_usb_cap.bFunctionalitySupport))
    print("      bU1devExitLat:         {:d}".format(ss_usb_cap.bU1DevExitLat))
    print("      bU2devExitLat:         {:d}".format(ss_usb_cap.bU2DevExitLat))


def print_bos(handle: ct.POINTER(usb.device_handle)):
    bos = ct.POINTER(usb.bos_descriptor)()
    ret = usb.get_bos_descriptor(handle, ct.byref(bos))
    if ret < 0:
        return
    bos = bos[0]

    print("  Binary Object Store (BOS):")
    print("    wTotalLength:            {:d}".format(bos.wTotalLength))
    print("    bNumDeviceCaps:          {:d}".format(bos.bNumDeviceCaps))

    for i in range(bos.bNumDeviceCaps):
        dev_cap: ct.POINTER(usb.bos_dev_capability_descriptor) = bos.dev_capability[i]

        if dev_cap[0].bDevCapabilityType == usb.LIBUSB_BT_USB_2_0_EXTENSION:

            usb_2_0_extension = ct.POINTER(usb.usb_2_0_extension_descriptor)()
            ret = usb.get_usb_2_0_extension_descriptor(None, dev_cap,
                                                       ct.byref(usb_2_0_extension))
            if ret < 0:
                return

            print_2_0_ext_cap(usb_2_0_extension[0])
            usb.free_usb_2_0_extension_descriptor(usb_2_0_extension)

        elif dev_cap[0].bDevCapabilityType == usb.LIBUSB_BT_SS_USB_DEVICE_CAPABILITY:

            ss_dev_cap = ct.POINTER(usb.ss_usb_device_capability_descriptor)()
            ret = usb.get_ss_usb_device_capability_descriptor(None, dev_cap,
                                                              ct.byref(ss_dev_cap))
            if ret < 0:
                return

            print_ss_usb_cap(ss_dev_cap[0])
            usb.free_ss_usb_device_capability_descriptor(ss_dev_cap)

    usb.free_bos_descriptor(ct.byref(bos))


def print_interface(interface):
    for i in range(interface.num_altsetting):
        print_altsetting(interface.altsetting[i])


def print_configuration(config: usb.config_descriptor):
    print("  Configuration:")
    print("    wTotalLength:            {:d}".format(config.wTotalLength))
    print("    bNumInterfaces:          {:d}".format(config.bNumInterfaces))
    print("    bConfigurationValue:     {:d}".format(config.bConfigurationValue))
    print("    iConfiguration:          {:d}".format(config.iConfiguration))
    print("    bmAttributes:            {:02x}h".format(config.bmAttributes))
    print("    MaxPower:                {:d}".format(config.MaxPower))
    for i in range(config.bNumInterfaces):
        print_interface(config.interface[i])


def print_device(dev: ct.POINTER(usb.device), handle: ct.POINTER(usb.device_handle)):
    global verbose

    string_descr = ct.create_string_buffer(256)

    device_speed = usb.get_device_speed(dev)
    if device_speed == usb.LIBUSB_SPEED_LOW:
        speed = "1.5M"
    elif device_speed == usb.LIBUSB_SPEED_FULL:
        speed = "12M"
    elif device_speed == usb.LIBUSB_SPEED_HIGH:
        speed = "480M"
    elif device_speed == usb.LIBUSB_SPEED_SUPER:
        speed = "5G"
    elif device_speed == usb.LIBUSB_SPEED_SUPER_PLUS:
        speed = "10G"
    else:
        speed = "Unknown"

    desc = usb.device_descriptor()
    ret = usb.get_device_descriptor(dev, ct.byref(desc))
    if ret < 0:
        print("failed to get device descriptor", file=sys.stderr)
        return

    print("Dev (bus {}, device {}): {:04X} - {:04X} speed: {}".format(
        usb.get_bus_number(dev), usb.get_device_address(dev),
        desc.idVendor, desc.idProduct, speed))

    if not handle:
        handle = ct.POINTER(usb.device_handle)()
        usb.open(dev, ct.byref(handle))

    if handle:
        if desc.iManufacturer:
            ret = usb.get_string_descriptor_ascii(handle, desc.iManufacturer,
                                                  ct.cast(string_descr, ct.POINTER(ct.c_ubyte)),
                                                  ct.sizeof(string_descr))
            if ret > 0:
                print("  Manufacturer:              {}".format(string_descr.value.decode()))

        if desc.iProduct:
            ret = usb.get_string_descriptor_ascii(handle, desc.iProduct,
                                                  ct.cast(string_descr, ct.POINTER(ct.c_ubyte)),
                                                  ct.sizeof(string_descr))
            if ret > 0:
                print("  Product:                   {}".format(string_descr.value.decode()))

        if verbose and desc.iSerialNumber:
            ret = usb.get_string_descriptor_ascii(handle, desc.iSerialNumber,
                                                  ct.cast(string_descr, ct.POINTER(ct.c_ubyte)),
                                                  ct.sizeof(string_descr))
            if ret > 0:
                print("  Serial Number:             {}".format(string_descr.value.decode()))

    if verbose:
        for i in range(desc.bNumConfigurations):
            config = ct.POINTER(usb.config_descriptor)()
            ret = usb.get_config_descriptor(dev, i, ct.byref(config))
            if ret != usb.LIBUSB_SUCCESS:
                print("  Couldn't retrieve descriptors")
                continue
            print_configuration(config[0])
            usb.free_config_descriptor(config)

        if handle and desc.bcdUSB >= 0x0201:
            print_bos(handle)

    if handle:
        usb.close(handle)


if __name__.rpartition(".")[-1] == "__main__":
    usb.init(None)
    devs = ct.POINTER(ct.POINTER(usb.device))()
    cnt = usb.get_device_list(None, ct.byref(devs))
    # print('cnt is ', cnt)
    for i in range(cnt):
        print_device(devs[i], None)

    print('devs value ', devs[5])
    usb.free_device_list(devs, 1)
    usb.exit(None)


