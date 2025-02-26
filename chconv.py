import sys
import zhconv

if len(sys.argv) != 3:
    print('chconv input ouput')
    exit()

update = {'妳':'你'}
old = open(sys.argv[1],'r',encoding='utf-8')
new = open(sys.argv[2],'w',encoding='utf-8')
try:
    temp = old.read()
except:
    old.close()
    old = open(sys.argv[1],'r',encoding='gbk')
    temp = old.read()
temp = zhconv.convert(temp,'zh-cn',update)
new.write(temp)
old.close()
new.close()