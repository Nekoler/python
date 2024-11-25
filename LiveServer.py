#!/usr/bin/env python

import psutil
import qrcode
import subprocess

ip = psutil.net_if_addrs()['wlan2'][0][1]
qr = qrcode.QRCode(border=1)
qr.add_data(f'http://{ip}:8080')
qr.print_ascii(tty=True)
cmd = ['live-server','--no-browser','--watch=**/*.html','/data/data/com.termux/files/home/code/Papers']
subprocess.run(cmd)
