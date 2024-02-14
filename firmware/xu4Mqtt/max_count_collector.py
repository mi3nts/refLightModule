import pandas as pd
import pandas as pd
from mintsXU4 import mintsOptics as mO

max_cap=65535.0
devicesPresent, deviceIDs = mO.checkingDevicePresence()
deviceID,device             = mO.openDevice(deviceIDs,0)

def max_count_collector(device):
    result_df = pd.DataFrame(columns=['Integration Time', 'Maximum'])
    for integration_time in range(500000, 6000001, 500000):
        illuminated_spectrum = device.get_formatted_spectrum(integration_time)
        maximum = max(illuminated_spectrum)

        result_df = result_df.append({'Integration Time': integration_time, 'Maximum': maximum}, ignore_index=True)

    # Find the maximum value closest to 75% of max cap
    closest_to_75_percent = result_df.iloc[(result_df['Maximum'] - 0.75 * max_cap).abs().argsort()[0]]

    return closest_to_75_percent['Integration Time']

