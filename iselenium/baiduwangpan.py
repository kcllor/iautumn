"""
    selenium模拟下载保存在百度网盘中的字体分享
"""
# -*- coding: UTF-8 -*-
import time
import base64

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


def process():
    # 百度网盘用户名
    username = 'abc@163.com'
    # 百度网盘密码
    password = 'password'

    driver = webdriver.Chrome(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
    driver.implicitly_wait(5)
    driver.get("https://ziyouziti.com/index-ziti-xiazai-id-93.html")
    driver.maximize_window()

    # 给浏览器增加cookie,绕过百度人机验证,注意调用方法 refresh()
    driver.add_cookie({'name': 'BAIDUID', 'value': '1111'})
    driver.add_cookie({'name': 'BDUSS', 'value': '1111'})
    driver.refresh()
    time.sleep(3)

    download_url = driver.find_element_by_class_name('c666').text
    verify_code = driver.find_element_by_class_name('info').text
    print(download_url, '---', verify_code)

    driver.get(download_url)
    access_code = driver.find_element_by_id('accessCode')
    access_code.clear()
    access_code.send_keys(verify_code)
    current_window = driver.current_window_handle
    print('current_window', current_window)
    print('click button:', driver.find_element_by_class_name('g-button-right').text)
    driver.find_element_by_class_name('g-button-right').click()
    # 同一个页面内跳转，可以加个等待时间，防止页面渲染过慢导致获取不到按钮问题
    time.sleep(3)
    all_window = driver.window_handles
    print('all_window', all_window)
    for window in all_window:
        if window != current_window:
            driver.switch_to(window)
    ele_download = driver.find_element_by_class_name('g-button-right')
    print('save button:', ele_download.id, ele_download.text, ele_download.location)
    ele_download.click()
    time.sleep(2)
    # div弹窗注意用xpath进行获取， 根据className获取不到
    # 模拟账号登录 - 输入用户名
    ele_username = driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_11__userName"]')
    ele_username.clear()
    for w in username:
        ele_username.send_keys(w)
        time.sleep(0.2)
    time.sleep(1)

    # 模拟账号登录 - 输入密码
    ele_password = driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_11__password"]')
    ele_password.clear()
    for p in password:
        ele_password.send_keys(p)
        time.sleep(0.4)
    time.sleep(2)

    # 模拟账号登录 - 登录
    ele_submit = driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_11__submit"]')
    # 模拟鼠标移动
    ActionChains(driver).move_to_element(ele_submit).perform()
    # location = ele_submit.location
    # print('ele_submit location:', location.get('x'), location.get('y'))
    # ActionChains(driver).move_by_offset(location.get('x'), location.get('y'))
    time.sleep(1)
    ele_submit.click()
    time.sleep(3)

    # 保存到网盘
    ele_save = driver.find_element_by_xpath('//*[@id="fileTreeDialog"]/div[3]/a[2]/span')
    ele_save.click()

    # 下载到本地
    # ele_cancel = driver.find_element_by_xpath('//*[@id="fileTreeDialog"]/div[3]/a[1]/span')
    # ele_cancel.click()
    # ele_download = driver.find_element_by_xpath(
    #     '//*[@id="layoutMain"]/div[1]/div[1]/div/div[2]/div/div/div[2]/a[2]/span/span')
    # ele_download.click()

