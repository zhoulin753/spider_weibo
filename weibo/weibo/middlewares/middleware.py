# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# time:2018/10/8


import time
from fake_useragent import UserAgent
from scrapy.http import HtmlResponse

'''
这个文件是专门处理我们的request和response的，当有新的url需要请求时，都会来到这个中间件，
当有新的response时，都会来到这个中间件，来处理，所以我们可以在请求要发送出去之前，来到这处理
同理response也是一样的！
注意：在下载中间件中我们有三个固定的方法：process_request，process_response,process
'''


class JavaScriptMiddleware(object):
    # page_image = 0

    def process_request(self, request, spider):

        if spider.name == "text":
            '''
            这个是用phantomjs这个无页面的浏览器来发送我们的请求，但是这个浏览器爬取页面比较慢，需要重新
            择优,当process_request这个方法当返回response对象时，直接跳到process_response方法进行response
            传递
            '''
            spider.driver.get(request.url)  # 发送url这个请求
            js = "var q=document.body.scrollTop=10000"
            spider.driver.execute_script(js)  # 可执行js，模仿用户操作。此处为将页面拉至最底端。
            body = spider.driver.page_source  # 返回的页面html
            spider.driver.save_screenshot('new.png')
            print("访问" + request.url)
            # 封装成response对象，到时我们可以xpath，css，
            return HtmlResponse(spider.driver.current_url, body=body, encoding='utf-8', request=request)
        else:
            return None

    def process_response(self, request, response, spider):

        '''
        这个函数是专门处理我们的response，我们要判断，如果这个url大于90，那么我们就可以判断出类似与
        https://weibo.com/a/aj/transform/loadingmoreunlogin?ajwvr=6&category=1760&page=8&lefnav=0&cursor=
        这种的url，那么我们就要进行重新处理，就要精要response_new这个函数
        '''

        if len(response.url) < 90:
            return response
        else:
            response = self.response_new(response.url, request)
            return response

    def response_new(self, response_url, request):
        # 这个函数是处理ajxa的数据，拿到的字符串转变成html对象
        import requests
        # 重新获取url返回的数据
        re = requests.get(response_url)
        re_text = eval(re.text)['data']
        # response=Selector(text=re_text)
        b = '\\'
        print('find:', re_text.find(b))
        '''
        如果发现'\\'这个字符串的话，那么我们就要就爱你跟这个字符串中的都去掉，重新组装成url，不然返回的数据报错
        '''
        if re_text.find(b) > 0:
            new_re_text_list = re_text.split(b)
            re_text = ''.join(new_re_text_list)
        return HtmlResponse(url=response_url, body=re_text, encoding='utf8', request=request)


class RandomUserAgent(object):

    def __init__(self, crawler):
        super(RandomUserAgent, self).__init__()
        """
        创建一个useragent的对象，然后我们可以从中随机获取useragent，
        self.ua.random 随机获取ie，chrom，firfox的useragent
        self.us.ie 随机获取ie的useragent
        """
        self.ua = UserAgent()
        # 获取我们sittings中的数据
        self.ua_type = crawler.settings.get('RANSOM_UA_TYPE', 'random')

    @classmethod
    def from_crawler(cls, crawler):
        # 当创建这个方法时，先运行这个类方法，之后将运行这个__init__这个方法，将这个cls==》self
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)

        # 设置我们的request头
        adder = self.get_ip().__next__()

        request.meta['proxy'] = adder

        request.headers.setdefault('User-Agent', get_ua())
        return None

    def process_response(self, request, response, spider):
        return response

    def get_ip(self):
        with open(r'C:\Users\admin\PycharmProjects\spider-dome\weibo\weibo\add.text', 'r+') as f:
            adder_list = f.read().split('\n')

        for i in adder_list:
            yield i
