# RaspberryPiZeroW_CarAndBall
### Raspberry Pi Zero W v1.1
- Single Core 1 Ghz ARM
- 512 Shared RAM GPU
- Mini HDMI OTG
- Micro USE x2

### Ref. Docs:
- https://leanpub.com/rpcultra/read#leanpub-auto-the-jsn-sr04t-sensor
- https://www.raspberrypi.com/products/raspberry-pi-zero-w/
- https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#raspberry-pi-zero-w

### To Configure the wireless connection priority
Edit the Wi-Fi Configuration File:
```
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```

Configure Network Priorities:
(Higher numbers have higher priority)
```
network={
  ssid="homeNetwork"
  psk="homePassword"
  key_mgmt=WPA-PSK
  priority=2
}

network={
  ssid="workNetwork"
  psk="workPassword"
  key_mgmt=WPA-PSK
  priority=1
}
```

