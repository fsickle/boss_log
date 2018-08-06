import os
import requests
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
import time
import random
import pymongo
import base64


class Login():
    def __init__(self, proxy=None):
        self.headers = {
            'Proxy-Authorization': self.get_proxy(),
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36',
            'referer': 'https://www.zhipin.com /',
        }
        self.session = requests.Session()
        self.client = pymongo.MongoClient('localhost')
        self.db = self.client['jobs']

    def get_proxy(self):
        proxyUser = 'H74274906A74PP2D'
        proxyPass = 'EA516E778B9E0A75'
        end = proxyUser + ":" + proxyPass
        a = base64.b64encode(end.encode('utf-8')).decode('utf-8')
        proxy = "Basic " + a
        return proxy

    def start_requests(self):
        url = 'https://login.zhipin.com/?ka=header-login'
        response = self.session.get(url, headers=self.headers)
        return response.text

    def get_key(self, content):
        soup = BeautifulSoup(content, 'lxml')
        img_value = soup.select('#wrap div.sign-wrap div.sign-form.sign-sms form div.form-row.row-code input')[1]
        img_value = img_value['value']
        return img_value

    def download_img(self, key):
        img_url = 'https://login.zhipin.com/captcha/?randomKey=' + key
        headers = self.headers.copy()
        headers['refer'] = 'https://login.zhipin.com/?ka=header-login'
        response = self.session.get(img_url, headers=headers)
        print('开始下载图片')
        file_path = '{0}/captcha.{1}'.format(os.getcwd(), 'png')
        print(file_path)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        captcha = input('看图验证码(看不清请输入 no)：')
        if captcha == 'no':
            return self.download_img(key)
        print('你输入的验证码是：%s'% captcha)
        return captcha

    def send_sms(self, key, value):
        url = 'https://login.zhipin.com/registe/sendSms.json'
        form_data = {
            'pk': 'cpc_user_sign_up',
            'regionCode': '+86',
            'phone': '18328592041',
            'captcha': value,
            'randomKey': key,
            'phoneCode': '',
            'smsType': '1',
        }
        headers = self.headers.copy()
        headers['refer'] = 'https://login.zhipin.com/?ka=header-login'
        headers['x-requested-with'] = 'XMLHttpRequest'
        response = self.session.post(url, headers=headers, data=form_data)
        print(response.text)
        if response.status_code == 200:
            print('发送成功')
        code = input('手机验证码(未收到请输入 no)：')
        if code == 'no':
            time.sleep(61)
            return self.send_sms(key, value)
        return code

    def login_in(self, key, value, code):
        url = 'https://login.zhipin.com/login/phone.json'
        form_data = {
            'pk': 'cpc_user_sign_up',
            'regionCode': '+86',
            'phone': '18328592041',
            'captcha': value,
            'randomKey': key,
            'phoneCode': code,
            'smsType': '1',
        }
        headers = self.headers.copy()
        headers['refer'] = 'https://login.zhipin.com/?ka=header-login'
        headers['x-requested-with'] = 'XMLHttpRequest'
        response = self.session.post(url, headers=headers, data=form_data)
        print(response.text)
        if response.status_code == 200:
            print('登陆成功')
            return True
        else:
            print('失败')
            return False

    def parse_index(self, n):
        index_url = 'https://www.zhipin.com/c101270100/h_101270100'
        query = {
            'query': 'python',
            'page': str(n),
            'ka': 'page-' + str(n),
        }
        headers = self.headers.copy()
        #headers['refer'] = 'https://www.zhipin.com/c101270100/h_101270100/?query=python'
        session = self.session
        response = session.get(index_url, headers=headers, params=query)
        return response.text

    def parse(self, content):
        soup = BeautifulSoup(content, 'lxml')
        hrefs = soup.select('#main > div > div.job-list > ul > li > div > div.info-primary > h3 > a')
        for href in hrefs:
            job_url = 'https://www.zhipin.com' + href['href']
            time.sleep(random.random())
            item = self.parse_job(job_url)
            self.save_to_mongo(item)


    def parse_job(self, job_url):
        session = self.session
        headers = self.headers.copy()
        response = session.get(job_url, headers=headers)
        content = pq(response.text)
        item = dict()
        item['job'] = content('#main div.job-banner div div div.info-primary div.name h1').text()
        item['salary'] = content('#main div.job-banner div div div.info-primary div.name span').text()
        item['base'] = content('#main div.job-banner div div div.info-primary p').text()
        item['describe'] = content('#main div.job-box div div.job-detail div.detail-content div:nth-child(1) div.text').text()
        item['team'] = content('#main div.job-box div div.job-detail div.detail-content div:nth-child(2) div.job-tags').text()
        item['company'] = content('#main div.job-box div div.job-detail div.detail-content div.job-sec.company-info div').text()
        item['url'] = url
        item['location'] = content('#main div.job-box div div.job-detail div.detail-content div:nth-child(6) div div.location-address').text()
        return item

    def save_to_mongo(self, item):
        if self.db['boss_jobs'].insert(item):
            print('存储到MongoDB', item)
            return True
        return False


if __name__ == '__main__':
    s = Login()
    html = s.start_requests()
    key = s.get_key(html)
    captcha = s.download_img(key)
    code = s.send_sms(key, captcha)
    result = s.login_in(key, captcha, code)
    if result:
        for i in range(1, 50):
            content = s.parse_index(i)
            s.parse(content)
