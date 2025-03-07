#!/usr/bin/env python

import psutil
import qrcode
import subprocess

ip = psutil.net_if_addrs()['wlan2'][0][1]
qr = qrcode.QRCode(border=1)
qr.add_data(f'MPEsocat socat TCP-LISTEN:15567,fork TCP:{ip}:8080')
qr.print_ascii(tty=True)
subprocess.run(['socat','TCP-LISTEN:8080,fork','TCP:localhost:15567'])
