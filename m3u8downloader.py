import os
import m3u8
from sys import argv
from Crypto.Cipher import AES
from threading import Thread,active_count
from requests import session,Session,adapters

def m3u8_handler(url:str,sess:Session):
    with sess.get(url) as m3u8_file:
        m3u8_text = m3u8.loads(m3u8_file.text,url)
    return [i.absolute_uri for i in m3u8_text.segments],m3u8_text.keys[0]

def create_aes(key_iv:m3u8.Key,sess:Session):
    with sess.get(key_iv.absolute_uri) as key_file:
        key = key_file.content
        if key_iv.iv:
            iv = key_iv.iv[2:].encode()
        else:
            iv = b'0000000000000000'
    return AES.new(key,AES.MODE_CBC,iv)

def downloader(url:str,tmp_dir:str,ts_name:str,sess:Session):
    with open(f'{tmp_dir}/{ts_name}','wb') as ts_local:
        with sess.get(url) as ts_online:
            ts_local.write(ts_online.content)

def ts_handler(filename:str,tmp_dir:str,url_list:list,key:m3u8.Key,sess:Session):
    with open(f'{filename}','wb') as video:
        if key:
            aes = create_aes(key,sess)
            for i in url_list:
                with open(f"{tmp_dir}/{i.split('/')[-1]}",'rb') as ts_local:
                    video.write(aes.decrypt(ts_local.read()))
        else:
            for i in url_list:
                with open(f"{tmp_dir}/{i.split('/')[-1]}",'rb') as ts_local:
                    video.write(ts_local.read())

def create_dir(tmp_dir:str):
    if not os.path.isdir(tmp_dir):
        os.mkdir(tmp_dir)

def remove_dir(filename:str,tmp_dir:str):
    os.remove(f'tmp_{filename}')
    for i in os.listdir(tmp_dir):
        os.remove(f'{tmp_dir}/{i}')
    os.removedirs(tmp_dir)

def main(url:str,filename:str):
    tmp_dir = f'{filename}_tmp'
    create_dir(tmp_dir)
    with session() as sess:
        sess.timeout = 5
        sess.mount('http', adapters.HTTPAdapter(max_retries=5))
        ts_list,key = m3u8_handler(url,sess)
        for i in ts_list:
            Thread(target=downloader,args=(i,tmp_dir,i.split('/')[-1],sess)).start()
            while active_count() > 16:
                pass
    while active_count() != 1:
        pass
    ts_handler(f'tmp_{filename}',tmp_dir,ts_list,key,sess)
    os.system(f'ffmpeg -i tmp_{filename} -c copy {filename}')
    remove_dir(filename,tmp_dir)

main(argv[1],argv[2])
