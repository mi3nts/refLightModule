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
- I2C Addresses
  - BME280: 77 and possibly 76 
  - AS7265x: 49
  - SCD30: 61
  - LTR390: maybe 10 
  - INA219: 40
```
teamlary@teamlary-ODROID-H3:~$ sudo i2cdetect -y -r 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
10: 10 -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: 40 -- -- -- -- -- -- -- -- 49 -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- 61 -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
70: -- -- -- -- -- -- 76 77
```


**Installing Network Driver on H3**
The following process s extracted from the following source: https://wiki.odroid.com/odroid-h3/hardware/install_ethernet_driver_on_h3plus



1. **BIOS Settings and Network Configuration**
   - Ensure that all BIOS settings are properly configured.
   - Set all network itineraries to true or enabled.

2. **Download the Realtek Network Driver**
   - Visit [Realtek's official website](https://www.realtek.com/en/component/zoo/category/network-interface-controllers-10-100-1000m-gigabit-ethernet-pci-express-software).
   - Download the "2.5G/5G Ethernet LINUX driver r8125" suitable for kernel up to version 6.4.

3. **Extract and Install the Driver**
   - Open a terminal and navigate to the directory where the downloaded driver file is located.
   - Extract the driver using the following commands:
     ```bash
     tar -xjf r8125-9.012.04.tar.bz2
     cd r8125-9.012.04
     ```
   - Install necessary build tools:
     ```bash
     sudo apt install build-essential
     ```
   - Run the installation script:
     ```bash
     sudo ./autorun.sh
     ```

4. **Check Network Hardware Visibility**
   - Confirm that the network hardware is visible by running the following command in the terminal:
     ```bash
     sudo lshw -C network
     ```

   Example output:
```
[sudo] password for teamlary: 
  *-network                 
       description: Ethernet interface
       product: RTL8125 2.5GbE Controller
       vendor: Realtek Semiconductor Co., Ltd.
       physical id: 0
       bus info: pci@0000:01:00.0
       logical name: enp1s0
       version: 05
       serial: 00:1e:06:45:24:54
       size: 1Gbit/s
       capacity: 1Gbit/s
       width: 64 bits
       clock: 33MHz
       capabilities: pm msi pciexpress msix vpd bus_master cap_list ethernet physical tp 10bt 10bt-fd 100bt 100bt-fd 1000bt-fd autonegotiation
       configuration: autonegotiation=on broadcast=yes driver=r8125 driverversion=9.011.01-NAPI duplex=full ip=192.168.20.127 latency=0 link=yes multicast=yes port=twisted pair speed=1Gbit/s
       resources: irq:16 ioport:4000(size=256) memory:7fe00000-7fe0ffff memory:7fe10000-7fe13fff
  *-network
       description: Ethernet interface
       product: RTL8125 2.5GbE Controller
       vendor: Realtek Semiconductor Co., Ltd.
       physical id: 0
       bus info: pci@0000:02:00.0
       logical name: enp2s0
       version: 05
       serial: 00:1e:06:45:24:55
       capacity: 1Gbit/s
       width: 64 bits
       clock: 33MHz
       capabilities: pm msi pciexpress msix vpd bus_master cap_list ethernet physical tp 10bt 10bt-fd 100bt 100bt-fd 1000bt-fd autonegotiation
       configuration: autonegotiation=on broadcast=yes driver=r8125 driverversion=9.011.01-NAPI latency=0 link=no multicast=yes port=twisted pair
       resources: irq:17 ioport:3000(size=256) memory:7fd00000-7fd0ffff memory:7fd10000-7fd13fff
  *-network
       description: Wireless interface
       physical id: 2
       bus info: usb@1:1
       logical name: wlx7cdd90adb4f8
       serial: 7c:dd:90:ad:b4:f8
       capabilities: ethernet physical wireless
       configuration: broadcast=yes driver=rt2800usb driverversion=5.15.0-91-generic firmware=0.36 ip=192.168.31.125 link=yes multicast=yes wireless=IEEE 802.11
```
**Enabling Network on H3**

At this point, the network card might be visible but disabled.

1. **Enable Ethernet Ports**
   - If not already done, activate both Ethernet ports using the following commands:
     ```bash
     sudo ifconfig enp1s0 up
     sudo ifconfig enp2s0 up
     ```

2. **Edit NetworkManager Configuration**
   - Open the NetworkManager configuration file in a text editor:
     ```bash
     sudo nano /etc/NetworkManager/NetworkManager.conf
     ```
   - Ensure the file has the following configuration:
     ```ini
     [main]
     plugins=ifupdown,keyfile

     [ifupdown]
     managed=true

     [device]
     wifi.scan-rand-mac-address=no

     [keyfile]
     unmanaged-devices=*,except:type:wifi,except:type:wwan,except:type:ethernet
     ```

   If the 'managed' key was false or the 'keyfile' was not available, update it accordingly.

3. **Reboot the H3**
   - After completing the steps, reboot the H3 for the changes to take effect.

This completes the process of installing and enabling the Realtek network driver on the H3 platform. Ensure that both Ethernet ports are activated, and the NetworkManager configuration is correctly set for optimal network functionality.

Source: [ODROID Wiki](https://wiki.odroid.com/odroid-h3/hardware/install_ethernet_driver_on_h3plus))**

