'''
Author: Dong Jiajun 2070928523@qq.com
Date: 2023-03-02 16:04:52
LastEditors: Dong Jiajun 2070928523@qq.com
LastEditTime: 2023-03-23 22:34:30
FilePath: \WebCrawler\main.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import random
import time
from selenium.common.exceptions import NoSuchElementException

url = 'https://www.wjx.cn/vm/hTeoRyZ.aspx#'
roll_distance = 0
option = webdriver.ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_experimental_option('useAutomationExtension', False)
start_driver = webdriver.Chrome(options=option)

myTime = time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))

def delay_roll(driver, t=0.5, distance=200): #延时+屏幕滚动
    global roll_distance
    roll_distance = roll_distance + distance
    js="var q=document.documentElement.scrollTop=" + str(roll_distance) #下拉像素(800是基于最顶端测算的距离)
    driver.execute_script(js)
    time.sleep(t)

def tiankong(driver, num, text):
    """_summary_

    Args:
        driver (Chrome): 打开浏览器对象
        num (int): 题号
        text (str): 答案
    """
    driver.find_element(By.XPATH, '//*[@id="q' + str(num) + '"]').send_keys(str(text))
    delay_roll(driver)
    
def is_open(driver) -> bool:
    """问卷是否已经开放

    Returns:
        bool: 开放为True
    """
    try: 
        driver.get(url)
        driver.find_element(By.XPATH, '//*[@id="divWorkError"]/div[2]/div[2]/p[1]')
        print("问卷未开放，打开时间：", \
            time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time())))
        return False
    except NoSuchElementException:
        return True
    
def autoWrite(url_survey, trytime=2):
    """主填写函数

    Args:
        trytime (int): 问卷数量
    """
    global start_driver
    answer=[["董佳俊", "3200102146", "13588034947"], ["王潇", "3210101769", "18004847579"]]
    
    while not is_open(start_driver):
        time.sleep(0.4)
        continue
    
    for i in range(trytime):
        print("正在自动填写")
        #防止被浏览器识别为脚本
        option = webdriver.ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(options=option)
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                            {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})
        driver.get(url_survey)
        time.sleep(0.2)
        
        tiankong(driver, 1, answer[i][0])
        tiankong(driver, 2, answer[i][1])
        tiankong(driver, 3, answer[i][2])

        driver.find_element(By.XPATH, '//*[@id="ctlNext"]').click()
        print('第'+str(i+1)+'次填写成功')
        time.sleep(1)
        
        # 模拟点击智能验证按钮 若无则直接跳过
        # 先点确认
        try:
            driver.find_element(By.XPATH,'//*[@id="layui-layer1"]/div[3]/a[1]').click()
            time.sleep(0.2)
        except:
            pass
        # 再点智能验证提示框，进行智能验证
        try:
            driver.find_element(By.XPATH, '//*[@id="SM_BTN_WRAPPER_1"]').click()
            time.sleep(0.2)
        except:
            pass
        print("end")
        
        driver.quit()
        time.sleep(0.2)
        
if __name__ == '__main__':
    autoWrite(url)
    start_driver.quit()
    time.sleep(1)
