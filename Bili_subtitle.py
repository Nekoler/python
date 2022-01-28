from json import loads
from requests import get

bv = '1hZ4y1S7U8'
info = loads(get(f'http://api.bilibili.com/x/web-interface/view?bvid={bv}',proxies={'http':'https://api.qiu.moe','https':'https://api.qiu.moe'}).text)
sub_list = info['data']['subtitle']['list']
for i in sub_list:
    print(i['lan'])
    print(i['subtitle_url'])
