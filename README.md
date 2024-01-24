# refLightModule
Contains firmware for mints reference light sensor

# Things to do 
- Auto boot from power cycling
- Bird Call data collection
- Low Cost Sensor firmware
  - IPS7100
  - BME280
  - SCD30
  - AS7265x
  - L --
  - Wi-Fi
  - **Rubber Sealant**
- Sky Cam SW
  - Sky cloud pixels
  - Cloud Classification 
    
## Installing the network driver on the H3
- Following this tutorial
  - https://wiki.odroid.com/odroid-h3/hardware/install_ethernet_driver_on_h3plus
 
## On Boot Up 
- Make sure all Bios Setting are set up 
  - Make sure all network itenaries are set to to true/ enabled
- Installing  the realtech network driver
From this link [https://www.realtek.com/en/component/zoo/category/network-interface-controllers-10-100-1000m-gigabit-ethernet-pci-express-software](link)
download the *2.5G/5G Ethernet LINUX driver r8125 for kernel up to 6.4* driver
- Extract and install the driver
  ```
  tar -xjf r8125-9.012.04.tar.bz2
  cd r8125-9.012.04
  sudo apt install build-essential
  sudo ./autorun.sh
  ```
  

 


 
   
