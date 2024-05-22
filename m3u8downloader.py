import os
import m3u8
from sys import argv
from requests import get
from threading import Thread,active_count
from Crypto.Cipher import AES,_mode_cbc

def downloader(filepath:str,url:str):
    with open(filepath,'wb') as ts_local,get(url) as ts_online:
        ts_local.write(ts_online.content)

def m3u8_handler(url:str):
    m3u8_file = m3u8.loads(get(url).text,url)
    return [i.absolute_uri for i in m3u8_file.segments],m3u8_file.keys

def create_aes(key_iv:m3u8.Key):
    key = get(key_iv.absolute_uri).content
    if key_iv.iv == None:
        iv = b'0000000000000000'
    else:
        iv = key_iv.iv[2:].encode()
    return AES.new(key,AES.MODE_CBC,iv)

def create_dir(tmp_dir):
    if not os.path.isdir(tmp_dir):
        os.mkdir(tmp_dir)

def ts_handle(filepath:str,ts_list:list,aescodec:_mode_cbc.CbcMode|None):
    with open(filepath,'wb') as video:
        if aescodec:
            for i in ts_list:
                with open(i,'rb') as ts_file:
                    video.write(aescodec.decrypt(ts_file.read()))
        else:
            for i in ts_list:
                with open(i,'rb') as ts_file:
                    video.write(ts_file.read())



segments,key_iv = m3u8_handler(argv[1])
tmp_dir = argv[2]+'_tmp'
create_dir(tmp_dir)
ts_list = [tmp_dir+'/'+i.split('/')[-1] for i in segments]
for i1,i2 in zip(ts_list,segments):
    while active_count() > 16:
        pass
    Thread(target=downloader,args=(i1,i2)).start()

while active_count() != 1:
    pass
if key_iv:
    ts_handle(argv[2],ts_list,create_aes(key_iv[0]))
else:
    ts_handle(argv[2],ts_list,None)
