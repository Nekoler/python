#!/usr/bin/env python

import os
import psutil
import qrcode
import subprocess

ip = psutil.net_if_addrs()['wlan2'][0][1]
qr = qrcode.QRCode(border=1)
qr.add_data(f'http://{ip}:5500')
qr.print_ascii(tty=True)
os.chdir('/data/data/com.termux/files/home/code/Papers')
cmd = ['five-server','--no-browser','--watch=**/*.html']
process = subprocess.run(cmd,stdout=subprocess.DEVNULL)
