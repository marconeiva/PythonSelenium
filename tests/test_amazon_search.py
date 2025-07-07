from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115 Safari/537.36")

    driver = webdriver.Chrome(options=options)

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    yield driver
    driver.quit()



def test_search_ps5_on_amazon(driver):
    driver.get("https://www.amazon.com/")

    wait = WebDriverWait(driver, 15)

    # Bypass cookie banner (optional)
    try:
        cookie_btn = wait.until(EC.element_to_be_clickable((By.ID, "sp-cc-accept")))
        cookie_btn.click()
    except:
        pass  # no banner

    search_box = wait.until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))
    search_box.send_keys("ps5 console")
    search_box.send_keys(Keys.RETURN)

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-main-slot")))

    # Scroll in steps to trigger lazy loading
    for _ in range(3):
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        time.sleep(2)

    # Target actual product titles
    results = driver.find_elements(By.CSS_SELECTOR, "h2 span.a-text-normal")
    driver.save_screenshot("screenshot.png")

    for i, r in enumerate(results):
        text = r.text.strip()
        print(f"[{i}] {text}")
        if "ps5" in text.lower():
            print("✅ MATCH FOUND")

    assert any("ps5" in r.text.lower() for r in results), "❌ No PS5-related titles found!"