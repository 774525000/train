import train

HOME_URL = 'https://www.12306.cn/index/index.html'
EMAIL = '774525000@qq.com'
PASSWORD = '199441201q'
CHAOJIYING_USERNAME = '774525000'
CHAOJIYING_PASSWORD = '199441201q'
CHAOJIYIN_APP_ID = 902929
PIC_TYPE = 9004

if __name__ == '__main__':
    train.run(HOME_URL, EMAIL, PASSWORD, CHAOJIYING_USERNAME, CHAOJIYING_PASSWORD, CHAOJIYIN_APP_ID, PIC_TYPE)
