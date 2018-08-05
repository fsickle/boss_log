import os
import requests
from bs4 import BeautifulSoup
import time


class Login():
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36',
        'referer': 'https://www.zhipin.com /',
    }
    session = requests.session()

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

    def parse_index(self):
        url = 'https://www.zhipin.com/job_detail/?query=python'
        headers = self.headers.copy()
        headers['refer'] = 'https://login.zhipin.com/?ka=header-login'
        session = self.session
        response = session.get()


if __name__ == '__main__':
    s = Login()
    html = s.start_requests()
    key = s.get_key(html)
    captcha = s.download_img(key)
    code = s.send_sms(key, captcha)
    s.login_in(ckey, captcha, code)