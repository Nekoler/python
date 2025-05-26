import sys
import zhconv

if len(sys.argv) != 2:
    print('chconv input')
    exit()

update = {'妳':'你'}
with open(sys.argv[1],'rb+') as text:
    temp = text.read()
    try:
        temp = temp.decode('utf-8')
    except:
        temp = temp.decode('gbk')
    temp = zhconv.convert(temp,'zh-cn',update)
    text.seek(0)
    text.truncate(0)
    text.write(temp.encode())
