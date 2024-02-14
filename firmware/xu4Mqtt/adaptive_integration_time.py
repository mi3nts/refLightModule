
import numpy as np
from mintsXU4 import mintsDefinitions as mD
from mintsXU4 import mintsOptics as mO
import max_count_collector

max_cap=65535.0
integration_time=mD.integrationTimeMicroSec

def adaptive_integration_time(data_list,device):
    global integration_time
    # Convert the list to numpy array
    data_array = np.array(data_list)
    
    # Calculate the 25th and 75th quantiles
    quantile_25 = np.quantile(data_array, 0.25)
    quantile_75 = np.quantile(data_array, 0.75)
    
    # Extract values within the 25th and 75th quantiles
    extracted_values = data_array[(data_array >= quantile_25) & (data_array <= quantile_75)]
    
    # Calculate the average of the extracted values
    average = np.mean(extracted_values)
    
    # Compare the average value to the max cap
    if 0.6 * max_cap <= average <= 0.9 * max_cap:
        mD.integrationTimeMicroSec = integration_time # Keep integration_time the same
    else:
        mD.integrationTimeMicroSec = max_count_collector(device)  


