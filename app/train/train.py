# -*- coding:utf-8  -*-

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from app.chaojiyin.chaojiying import Chaojiying_Client
from selenium.webdriver.support.ui import WebDriverWait
from app.utils.file import save_pic, get_pic
from selenium.webdriver.common.by import By
from app.utils.point import get_points
from selenium import webdriver
from time import sleep


class Train:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()

    def enter_login(self):
        try:
            self.driver.get(self.url)
            self.driver.maximize_window()
            # 进入登录页
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.login-code-main .code-pic')))

            # 切换登录方式
            self.driver.find_element_by_css_selector(".login-hd .login-hd-account a").click()
        except Exception as e:
            print(e)
            raise e

    def get_pic(self):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '#J-loginImg')))
            return element.get_attribute('src')
        except Exception as e:
            print(f"获取验证码失败:{e}")
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
            for item in arr:
                ActionChains(self.driver).move_to_element_with_offset(element, int(item[0]),
                                                                      int(item[1])).click().perform()
                sleep(1)
        except Exception as e:
            print(e)
            raise e

    def login(self):
        try:
            self.driver.find_element_by_css_selector('#J-login').click()
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
        # 获取图片
        im = get_pic()
        # 获取打码结果
        res = chaojiying.PostPic(im, pic_type)
        # 获取坐标
        arr = get_points(res)
        # 输入账号密码
        train.enter_account(email, password)
        # 点击验证码
        train.click_pic(arr)
        # 登录
        train.login()
