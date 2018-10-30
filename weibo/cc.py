import time
import requests
import re
from urllib.parse import unquote
url = '''https://passport.weibo.com/visitor/visitor?entry=miniblog&a=enter&url=https%3A%2F%2Fweibo.com%2Fttarticle%2Fp%2Fshow%3Fid%3D2309404298262772365509&domain=.weibo.com&ua=php-sso_sdk_client-0.6.28&_rand={}'''.format(time.time())
print(time.time())
r = requests.get(url,)

urls = re.search(r'https://weibo.com/ttarticle/p/show\?id=(\d+)',r.content.decode('gbk')).group()
new_r = requests.head(urls,)
print(new_r.status_code)
print(time.time())
r1 = requests.post('https://weibo.com/ttarticle/p/show?id=2309404300906412821509')
print(r1.url)
print(unquote(r1.url,'utf8'))