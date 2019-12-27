from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import base64


def run(email, password, chaojiying_name, chaojiying_pass, chaojiying_app_id):
    try:
        driver = webdriver.Chrome()

        # 进入首页
        driver.get('https://www.12306.cn/index/index.html')
        driver.maximize_window()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'J-header-login')))

        # 获取登录按钮点击
        driver.find_element_by_css_selector("#J-header-login a").click()

        # 进入登录页
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.login-code-main .code-pic')))

        # 切换登录方式
        driver.find_element_by_css_selector(".login-hd .login-hd-account a").click()

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#J-loginImg')))
        # 输入账号密码
        driver.find_element_by_css_selector("#J-userName").send_keys(email)
        driver.find_element_by_css_selector("#J-password").send_keys(password)

        # 获取验证码
        src_url = driver.find_element_by_css_selector("#J-loginImg").get_attribute('src')

        # 保存验证码图片
        with open('./static/pic.png', 'wb') as f:
            f.write(base64.b64decode(src_url.split(',')[1]))

        print("保存图片成功")
    except Exception as e:
        print("糟糕，获取失败")

    sleep(100)
