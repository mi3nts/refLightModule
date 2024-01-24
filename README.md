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
- Check that the Network HW is visible
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
At this point, it might show the network card although visible, but disabled.

- Enable both ethernet ports
```
sudo ifconfig enp1s0 up
sudo ifconfig enp2s0 up
```

- Edit the /etc/NetworkManager/NetworkManager.conf file so that it looks linke the following: 
```
[main]
plugins=ifupdown,keyfile

[ifupdown]
managed=true

[device]
wifi.scan-rand-mac-address=no

[keyfile]
unmanaged-devices=*,except:type:wifi,except:type:wwan,except:type:ethernet

```
In the case of a fresh ubuntu install managed key was false and the keyfile was not available.

- Reboot the H3











 


 
   
