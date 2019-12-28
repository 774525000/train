from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from train.chaojiyin.chaojiying import Chaojiying_Client
import base64
from time import sleep
from random import random


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
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#J-loginImg')))

            # 获取验证码
            return self.driver.find_element_by_css_selector("#J-loginImg").get_attribute('src')
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

    def click_img(self, arr):
        try:
            img = self.driver.find_element_by_css_selector("#J-loginImg")
            action = ActionChains(self.driver)
            for item in arr:
                action.move_to_element_with_offset(img, int(item[0]), int(item[1])).click().perform()
                sleep(random() + 0.5)
        except Exception as e:
            print(e)
            raise e

    @classmethod
    def default(cls, url, email, password, chaojiying_name, chaojiying_pass, chaojiying_app_id, pic_type):
        train = Train(url)
        train.enter_login()
        pic_src = train.get_pic()
        save_pic(pic_src)
        # 打码
        chaojiying = Chaojiying_Client(chaojiying_name, chaojiying_pass, chaojiying_app_id)
        im = open('./static/pic.png', 'rb').read()
        pic_str = chaojiying.PostPic(im, pic_type)['pic_str']
        arr = [item.split(',') for item in pic_str.split('|')]
        train.enter_account(email, password)
        train.click_img(arr)
