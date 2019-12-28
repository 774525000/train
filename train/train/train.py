from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from train.chaojiyin.chaojiying import Chaojiying_Client
import base64
from time import sleep
from random import randint


def save_pic(url):
    try:
        with open('./static/pic.png', 'wb') as f:
            f.write(base64.b64decode(url.split(',')[1]))
    except Exception as e:
        print(f"保存图片失败:{e}")
        raise e


class Train:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()

    def get_pic(self):
        try:
            element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#J-loginImg')))
            return element.get_attribute('src')
        except Exception as e:
            print(f"获取验证码失败:{e}")
            raise e

    def enter_login(self):
        try:
            self.driver.get(self.url)
            self.driver.maximize_window()
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'J-header-login')))

            # 获取登录按钮点击
            self.driver.find_element_by_css_selector("#J-header-login a").click()

            # 进入登录页
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.login-code-main .code-pic')))

            # 切换登录方式
            self.driver.find_element_by_css_selector(".login-hd .login-hd-account a").click()
        except Exception as e:
            print(e)
            raise e

    def enter_account(self, email, password):
        try:
            # 输入账号密码
            self.driver.find_element_by_css_selector("#J-userName").send_keys(email)
            self.driver.find_element_by_css_selector("#J-password").send_keys(password)
        except Exception as e:
            print(e)
            raise e

    def click_pic(self, arr):
        try:
            element = self.driver.find_element_by_css_selector("#J-loginImgArea")
            action = ActionChains(self.driver)
            for item in arr:
                action.move_to_element_with_offset(element, int(item[0]) + randint(5, 10),
                                                   int(item[1]) + randint(5, 10)).click().perform()
                sleep(randint(1, 3))
        except Exception as e:
            print(e)
            raise e

    def login(self):
        try:
            self.driver.find_element_by_css_selector('#J-login').click()
        except Exception as e:
            print(e)
            raise e

    def get_points(self, res):
        try:
            if res.get('pic_str'):
                pic_str = res['pic_str']
                return [item.split(',') for item in pic_str.split('|')]
        except Exception as e:
            print(e)
            raise e

    @classmethod
    def default(cls, url, email, password, chaojiying_name, chaojiying_pass, chaojiying_app_id, pic_type):
        train = cls(url)
        train.enter_login()
        # 获取验证码
        pic_src = train.get_pic()
        # 保存图片
        save_pic(pic_src)
        # 打码
        chaojiying = Chaojiying_Client(chaojiying_name, chaojiying_pass, chaojiying_app_id)
        with open('./static/pic.png', 'rb') as f:
            im = f.read()
        # 获取打码结果
        res = chaojiying.PostPic(im, pic_type)
        # 获取坐标
        arr = train.get_points(res)
        print(arr)
        # 输入账号密码
        train.enter_account(email, password)
        # 点击验证码
        train.click_pic(arr)
        # 登录
        train.login()

