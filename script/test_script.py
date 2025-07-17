from multiprocessing import Process
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import subprocess
import time

def run_instance(instance_id):
    chrome_options = Options()
    chrome_options.add_argument("--disable-search-engine-choice-screen")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-backgrounding-occluded-windows")
    chrome_options.add_argument("--disable-renderer-backgrounding")
    chrome_options.add_argument("--disable-background-timer-throttling")
    chrome_options.add_argument("--disable-backgrounding")
    chrome_options.add_argument("--autoplay-policy=no-user-gesture-required")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--disable-logging")

    service = Service(ChromeDriverManager().install(), log_path='NUL')
    service.creationflags = subprocess.CREATE_NO_WINDOW

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://relay.amazon.de/loadboard/search")
    driver.maximize_window()

    button_selector_xpath = "//p[contains(normalize-space(text()), 'refresh')]"

    while True:
        try:
            WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, button_selector_xpath))
            )
            button = driver.find_element(By.XPATH, button_selector_xpath)
            button.click()
        except Exception:
            pass
        time.sleep(14)

if __name__ == '__main__':
    processes = []
    for i in range(4):
        p = Process(target=run_instance, args=(i+1,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
