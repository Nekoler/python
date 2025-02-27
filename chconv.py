import sys
import zhconv

if len(sys.argv) != 3:
    print('chconv input ouput')
    exit()

update = {'妳':'你'}
with open(sys.argv[1],'rb') as old,open(sys.argv[2],'wb') as new:
    temp = old.read()
    try:
        temp = temp.decode('utf-8')
    except:
        temp = temp.decode('gbk')
    temp = zhconv.convert(temp,'zh-cn',update)
    new.write(temp.encode())
