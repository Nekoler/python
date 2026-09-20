import sys
import opencc

if len(sys.argv) != 2:
    print('chsconv input')
    exit()

conv = opencc.OpenCC('tw2sp')
mapping = {'妳': '你', '牠': '它'}
trans = str.maketrans(mapping)

with open(sys.argv[1], 'rb+') as text:
    temp = text.read()
    try:
        temp = temp.decode('utf-8')
    except:
        temp = temp.decode('gbk')
    temp = conv.convert(temp)
    temp = temp.translate(trans)
    text.seek(0)
    text.truncate(0)
    text.write(temp.encode())
