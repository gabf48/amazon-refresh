import time
from selenium import webdriver
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login import Login
from selenium.webdriver.chrome.options import Options


# Fișierul pentru configurarea browser-ului
@pytest.fixture(scope="session")
def browser():
    # Configurăm opțiunile pentru fiecare instanță de browser
    chrome_options = Options()
    chrome_options.add_argument("--disable-search-engine-choice-screen")
    chrome_options.add_argument("--window-size=1920,1080")  # Setează dimensiunea ferestrei

    # Aici se creează o instanță de browser per worker
    driver = webdriver.Chrome(options=chrome_options)

    yield driver  # Browser-ul este folosit în test
    driver.quit()  # La final se închide browser-ul


@pytest.mark.repeat(4)
def test_auto_refresh(browser, request):
    # Logăm worker-ul folosind un marker unic din pytest-xdist
    worker_id = request.config.getoption("--dist")  # Accesăm opțiunea de distribuire

    print(f"Running on worker {worker_id}")

    login = Login(browser)
    login.login()

    button_selector = "#utility-bar > div > div > div.refresh-and-chat-box > div > div.css-1vq46oc > div > button > span > span > svg"

    total_time = 8 * 3600  # 8 ore în secunde
    interval = 5  # interval de 5 secunde între clicuri
    max_attempts = total_time // interval  # numărul total de încercări în 8 ore

    print(f"Total time: {total_time} seconds")
    print(f"Max attempts: {max_attempts}")

    # Așteaptă încărcarea paginii și dă timp pentru apăsarea butonului
    time.sleep(30)

    # Loop pentru a apăsa butonul la fiecare 5 secunde
    for attempt in range(max_attempts):
        try:
            button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, button_selector))
            )
            button.click()
            print(f"Click pe buton efectuat. Încercarea {attempt + 1}")
        except Exception as e:
            print(f"Eroare la găsirea sau click pe buton la încercarea {attempt + 1}: {e}")

        # Așteaptă pentru următoarea încercare, dar se oprește după 8 ore sau dacă nu mai sunt încercări
        if attempt < max_attempts - 1:  # nu adăuga sleep după ultima încercare
            time.sleep(interval)
