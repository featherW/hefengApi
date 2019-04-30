import base64
import hashlib
import json
import time
import requests

class HefengApi(object):

    AQI_PREFIX = 'air'
    WEATHER_PREFIX = 'weather'

    def __init__(self, username='HE1904301129421782',
                 key='62fc176beb504921b983e6a0e0bfe376',
                 url='https://free-api.heweather.net/s6',
                 proxies='', verify=''):

        # 和风应用中的Username
        self.username = username

        # 和风应用中的Key
        self.key = key

        # 和风请求的基础url
        self.url = url

        # request请求的代理地址, 一般为默认值
        self.proxies = proxies

        # request请求的证书地址, 一般为默认值
        self.verify = verify

    def cal_sign(self, params, secret):
        r'''计算和风签名。

        :param params: url中的参数, 字典类型类型。
        :param secret: 和风的应用key。
        :return: 签名值
        '''

        canstring = ''
        params = sorted(params.items(), key=lambda item: item[0])
        for k, v in params:
            if (k != 'sign' and k != 'key' and v != ''):
                canstring += k + '=' + str(v) + '&'
        canstring = canstring[:-1]
        canstring += secret

        md5 = hashlib.md5(canstring.encode('utf-8')).digest()
        return base64.b64encode(md5)

    def request(self, prefix, location, type=None):
        r'''

        :param prefix: url前缀, 比如weather、air。
        :param location: 和风url参数中location字段。
        :param type: 和风url中请求类型字段，比如now、hourly。
        :return: 和风返回的数据, json格式
        '''

        params = {'location': location,
                  'username': self.username,
                  't': int(time.time())}
        params['sign'] = self.cal_sign(params, self.key)

        url = '%s/%s'%(self.url, prefix)
        if type != None:
            url = '%s/%s'%(url, type)

        kwargs = None
        if len(self.proxies) != 0:
            proxies = {
                'http': self.proxies,
                'https': self.proxies
            }
            kwargs['proxies'] = proxies
            if len(self.verify) != 0:
                kwargs['verify'] = self.verify

        if kwargs != None:
            rep = requests.get(url, params=params, data={}, **kwargs)
        else:
            rep = requests.get(url, params=params, data={})
        return json.loads(rep.text)

    def get_weather_with_lat_lon_now(self, lat, lon):
        r''' 根据经纬度获取天气实况

        :param lat: 纬度
        :param lon: 经度
        :return: 查询结果, json格式的object
        '''
        return self.request(self.WEATHER_PREFIX, '{},{}'.format(lat, lon),
                            'now')


if __name__ == '__main__':
    hefengApi = HefengApi()
    print(hefengApi.get_weather_with_lat_lon_now(121.561691284, 29.8253211975))



