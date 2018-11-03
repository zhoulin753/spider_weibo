import time
import requests
#import re

# url = '''https://passport.weibo.com/visitor/visitor?entry=miniblog&a=enter&url=https%3A%2F%2Fweibo.com%2Fttarticle%2Fp%2Fshow%3Fid%3D2309404298262772365509&domain=.weibo.com&ua=php-sso_sdk_client-0.6.28'''
# # print(time.time())
# r = requests.post(url,)
#
# urls = re.search(r'https://weibo.com/ttarticle/p/show\?id=(\d+)',r.content.decode('gbk')).group()
# datadict = {
#     'SINAGLOBAL':'3256254250610.868.1533378616439',
#     'SUBP':'0033WrSXqPxfM72-Ws9jqgMF55529P9D9WWKdSRrZ8dVHJ.AOAIcggUX',
#     'UOR':',,www.baidu.com',
#     'SUB':'_2AkMsjJAOf8NxqwJRmfgUzGzhaohxyQ7EieKa0GHVJRMxHRl-yj83qkAltRB6Bwy-4bsZ2jINrehvQk8VbH4o_24GsLwJ',
#     'YF-Page-G0':'1a5a1aae05361d646241e28c550f987',
#     'YF-V5-G0':'fec5de0eebb24ef556f426c61e53833b',
#     '_s_tentry':'-',
#     'Apache':'2536857901811.8267.1540539608026',
#     'ULV':'1540539608080:16:10:6:2536857901811.8267.1540539608026:1540364202943',
#     'WBStorage':'e8781eb7dee3fd7f|undefined'
#
#
# }
#
#
# new_r = requests.post(urls, json=datadict)
# # print(new_r.cookies.get_dict())
# print(urls)
# print(new_r.url)
# print(time.time())
#
# from urllib.parse import unquote
# url = '''https://passport.weibo.com/visitor/visitor?entry=miniblog&a=enter&url=https%3A%2F%2Fweibo.com%2Fttarticle%2Fp%2Fshow%3Fid%3D2309404298262772365509&domain=.weibo.com&ua=php-sso_sdk_client-0.6.28&_rand={}'''.format(time.time())
# print(time.time())
# r = requests.get(url,)
#
# urls = re.search(r'https://weibo.com/ttarticle/p/show\?id=(\d+)',r.content.decode('gbk')).group()
# new_r = requests.head(urls,)
# print(new_r.status_code)
# print(time.time())
# r1 = requests.post('https://weibo.com/ttarticle/p/show?id=2309404300906412821509')

#sess = requests.session()
#ret = sess.get('https://weibo.com/ttarticle/p/show?id=2309404298262772365509')
# r1 = requests.post('https://weibo.com/ttarticle/p/show?id=2309404298262772365509')

url = 'https://passport.weibo.com/visitor/visitor?entry=miniblog&a=enter&url=https%3A%2F%2Fweibo.com%2Fttarticle%2Fp%2Fshow%3Fid%3D2309404298262772365509&domain=.weibo.com&ua=php-sso_sdk_client-0.6.28&_rand={0}'.format(time.time())
url_3 = 'https://weibo.com/a/aj/transform/loadingmoreunlogin?ajwvr=6&category=1760&page=3&lefnav=0&cursor='
re = requests.get(url_3)
# https://passport.weibo.com/visitor/visitor?entry=miniblog&a=enter&url=https%3A%2F%2Fweibo.com%2Fttarticle%2Fp%2Fshow%3Fid%3D2309404298262772365509&domain=.weibo.com&ua=php-sso_sdk_client-0.6.28&_rand=1540993314.8047
#ret = sess.get('https://weibo.com/ttarticle/p/show?id=2309404298262772365509')

with open('a.html', 'w+') as f:
    f.write(re.content.decode('gbk'))

# print(time.time())
# print(unquote(r1.url,'utf8'))

