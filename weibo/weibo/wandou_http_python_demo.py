#encoding=UTF-8
import requests
import base64

# 请求头认证方式暂时不支持https协议
# 请通过添加ip白名单方式添加全局支持
# 添加白名单接口: https://h.wandouip.com/get/add-white-list?iplist=你的公网ip (登录状态下调用，公网ip请通过网络查询)

def base_code(username, password):
    str = '%s:%s' % (username, password)
    encodestr = base64.b64encode(str.encode('utf-8'))
    return '%s' % encodestr.decode()

if __name__ == '__main__':
    username = "1281263636@qq.com"  # 您的用户名
    password = "Zl8439736"  # 您的密码
    proxy_ip = "113.237.186.10"  # 代理ip，通过http://h.wandouip.com/get获得
    proxy_port = "766"  # 代理端口号
    head = {
        'Proxy-Authorization': 'Basic %s' % (base_code(username, password))
    }
    proxy = {
        'http': 'http://%s:%s' % (proxy_ip, proxy_port),
        'https': 'https://%s:%s' % (proxy_ip, proxy_port)
    }
    url = 'http://myip.ipip.net'
    try:
        text = requests.get('http://www.xicidaili.com/wn/', headers=head, proxies=proxy, timeout=5).text
        print(text)
    except Exception as e:
        print("Error: ", e)
