import selenium
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException

def browser_init():
    option = webdriver.ChromeOptions()
    browser = webdriver.Chrome(executable_path='/Library/Application Support/Google/chromedriver', chrome_options=option)
    return browser

def insta_login(browser):
    browser.get('https://www.instagram.com')

    #Find username/pass fields
    username = WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.XPATH, '//input[@name="username"]')))
    password = WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.XPATH, '//input[@name="password"]')))

    #input username and pass
    username.clear()
    username.send_keys('itanikarim')
    password.clear()
    password.send_keys('1995PPrr')

    #Login
    Login_button = WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginForm"]/div/div[3]'))).click()

    #Skip buttons
    not_now = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
    not_now2 = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()



print("everything ok")