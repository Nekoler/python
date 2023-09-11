#!/data/data/com.termux/files/usr/bin/python
from json import dumps
from qrcode import QRCode
from base64 import b64encode

idcard = open('id.txt')
for i in idcard.readlines():
    i = i.replace('\n','').split(' ')
    out = dumps({'name':i[0],'idcard':i[1]},ensure_ascii=False,separators=(',',':'))
    out = b64encode(out.encode()).decode()
    Qr = QRCode()
    Qr.border = 1
    Qr.add_data(out)
    Qr.make()
    print(i[0])
    Qr.print_ascii(tty=True)
