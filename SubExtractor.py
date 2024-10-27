import os
import sys
import time
import numpy
import zhconv
import difflib
import paddleocr
import subprocess
import multiprocessing

def sec_to_hms(s:float)->str:
    h,s = divmod(s,3600)
    m,s = divmod(s,60)
    s,ms = divmod(s,1)
    hms = f'{int(h):0>2}:{int(m):0>2}:{int(s):0>2}.{int(ms//0.001):0>3}'
    return hms

def frame_pipe(path:str)->subprocess.Popen:
    cmd = ['ffmpeg.cmd','-i',path,'-c:v','rawvideo','-pix_fmt','gray','-f','image2pipe','-']
    rawvideo = subprocess.Popen(cmd,stdout=subprocess.PIPE)
    return rawvideo

def cut_frame(frame:bytes)->numpy.ndarray:
    frame = numpy.frombuffer(frame,numpy.uint8)
    frame = frame.reshape((1080,1920))
    frame = numpy.vstack((frame[:216],frame[864:]))
    return frame

def ocr_engine()->paddleocr.PaddleOCR:
    rec_model_dir = 'D:/Portable/Bin/Scripts/Models/rec'
    det_model_dir = 'D:/Portable/Bin/Scripts/Models/det'
    cls_model_dir = 'D:/Portable/Bin/Scripts/Models/cls'
    Ocr = paddleocr.PaddleOCR(rec_model_dir=rec_model_dir,det_model_dir=det_model_dir,cls_model_dir=cls_model_dir,show_log=False)
    return Ocr

def trans_char(con:str)->str:
    con = con.upper()
    con = con.replace('“','"')
    con = con.replace('”','"')
    con = con.replace('‘',"'")
    con = con.replace('’',"'")
    con = zhconv.convert(con,'zh-cn')
    return con

def rec_char(line:multiprocessing.Queue,res:list)->None:
    Ocr = ocr_engine()
    while (item:=line.get()):
        sub = []
        if (items:=Ocr.ocr(item['con'],cls=False)[0]):
            for i in items:
                sub.append(i[-1][0])
            else:
                sub.append('\n')
                item['con'] = '\n'.join(sub)
                res.append(item)

def get_vtt(res:list)->str:
    res.sort(key=lambda x:x['num'])
    for i in res:
        i['con']=trans_char(i['con'])
    fps = 24000/1001
    duration = '{0} --> {1}\n'
    differ = difflib.SequenceMatcher()
    vtt_list = ['WEBVTT\n\n']
    start = res[0]
    for next in res:
        differ.set_seqs(start['con'],next['con'])
        if differ.ratio()<0.7:
            sub = duration.format(sec_to_hms(start['num']/fps),sec_to_hms(end['num']/fps))
            vtt_list.append(sub+start['con'])
            start = next
        end = next
    sub = duration.format(sec_to_hms(start['num']/fps),sec_to_hms(end['num']/fps))
    vtt_list.append(sub+start['con'])
    vtt = ''.join(vtt_list)
    return vtt

def main(Processor:int)->None:
    num = 0
    path = sys.argv[1]
    os.environ['PATH'] += 'D:/Portable/Bin/cuDNN;'
    line = multiprocessing.Queue(10)
    res = multiprocessing.Manager().list()
    pool = []
    for _ in range(Processor):
        pool.append(multiprocessing.Process(target=rec_char,args=(line,res)))
    for i in pool:
        i.start()
    time.sleep(4)
    rawvideo = frame_pipe(path)
    while (con:=rawvideo.stdout.read(1920*1080)):
        line.put({'num':num,'con':cut_frame(con)})
        num += 1
    for _ in range(Processor):
        line.put(False)
    for i in pool:
        i.join()
    with open(path[:-3]+'vtt','w',encoding='utf8') as sub:
        sub.write(get_vtt(list(res)))

if __name__=='__main__':
    main(2)