import time

from selenium.webdriver.common.by import By


class Login:

    def __init__(self, driver):
        self.driver = driver


    def login(self):
        self.driver.get('https://relay.amazon.de/loadboard/search')
        self.driver.maximize_window()
        self.driver.find_element(By.ID, 'ap_email').send_keys('poptransugamz@gmail.com')
        # self.driver.find_element(By.ID, 'continue').click()
        # self.driver.find_element(By.ID, 'ap_password').send_keys('amazon2024')
        # self.driver.find_element(By.ID, 'signInSubmit').click()




