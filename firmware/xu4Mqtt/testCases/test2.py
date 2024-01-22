from __future__ import annotations
from oceandirect.OceanDirectAPI import OceanDirectAPI, OceanDirectError
from oceandirect.od_logger import od_logger
from threading import Thread

logger = od_logger()

od = OceanDirectAPI()

device_count = od.find_usb_devices()
device_ids   = od.get_device_ids()

device_count = len(device_ids)

def get_spectra_single(device,numb_spectra):
    try: 
        device.set_scans_to_average(1)
        numb_pixel = len(device.get_formatted_spectrum()) 
        spectra_m = [[0 for x in range(numb_pixel)] for y in range(numb_spectra)]
        for i in range(numb_spectra):
            spectra_m[i] = device.get_formatted_spectrum()
        print(spectra_m[0:1])
        
        print("Rows")        
        print(len(spectra_m))
        print("Columns")        
        print(len(spectra_m[0]))

    except OceanDirectError as e:
        logger.error(e.get_error_details())   

print("Device IDs")
print(device_ids)  

print("Device Counts")
print(device_count)

device       = od.open_device(2)

print("Device:")
print(device)

serialNumber = device.get_serial_number()
print("Serial Number: %s" % serialNumber)


#if (device_count): 
#    for id in device_ids:
#        device       = od.open_device(id)
#        serialNumber = device.get_serial_number()
#        print("Serial Number: %s" % serialNumber)
        

        
#        int_time_us = 218 
#        numb_spectra = 4560
        
#        device.set_electric_dark_correction_usage(False)
#        device.set_nonlinearity_correction_usage(True)
#        device.set_integration_time(int_time_us)
        
#        print("Single Capture")
#        get_spectra_single(device,numb_spectra)
        
#        od.close_device(id)
        