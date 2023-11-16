## RPi

OS Version: Raspberry Pi OS (Legacy) with desktop

Debian Version:11

Kernel Version: 5.10

## Camera Driver Install:

https://docs.rs-online.com/c69c/A700000009169905.pdf

```commandline
sudo rpi-update a54fe46c85fd4a2155f2282454bee3c2a3d5b5eb
git clone https://github.com/INNO-MAKER/CAM-OV9281RAW-V2.git
sudo chmod -R a+rwx *
nano autoinstall_driver.sh 
````
Rename pi3_4 to pi_4
```
echo "System is 64 bit arch."
driverpath=./$version/$arch/pi3_4
driverpath=./$version/$arch/pi4
```

```commandline
./autoinstall_driver.sh
ls /dev
```

Should have video0

## Camera Mode Set

```commandline
sudo nano /boot/cmdline.txt
```
Add line:
`vc_mipi_ov9281.sensor_mode=0`

## OpenCV

```commandline
pip install opencv-python
sudo pip install opencv-python
```
