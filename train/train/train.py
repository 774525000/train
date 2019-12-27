from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import base64


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

    def get_pic(self, email, password):
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

            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#J-loginImg')))
            # 输入账号密码
            self.driver.find_element_by_css_selector("#J-userName").send_keys(email)
            self.driver.find_element_by_css_selector("#J-password").send_keys(password)

            # 获取验证码
            return self.driver.find_element_by_css_selector("#J-loginImg").get_attribute('src')
        except Exception as e:
            print(f"获取验证码失败:{e}")
            raise e

    @classmethod
    def default(cls, url, email, password):
        train = Train(url)
        pic_src = train.get_pic(email, password)
        save_pic(pic_src)
