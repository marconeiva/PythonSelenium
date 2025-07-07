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
    driver.get("https://www.amazon.com/-/en/")  # Force US-English

    wait = WebDriverWait(driver, 15)

    # Accept cookie banner if present
    try:
        cookie_btn = wait.until(EC.element_to_be_clickable((By.ID, "sp-cc-accept")))
        cookie_btn.click()
    except:
        pass  # No cookie banner

    # Perform search
    search_box = wait.until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))
    search_box.send_keys("ps5 console")
    search_box.send_keys(Keys.RETURN)

    # Wait for results container
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-main-slot")))

    # Simulate user scroll to trigger lazy loading
    for _ in range(3):
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        time.sleep(2)

    # Locate actual product titles
    results = driver.find_elements(By.CSS_SELECTOR, "h2 span.a-text-normal")

    # Save screenshot and result HTML for pipeline artifacts
    driver.save_screenshot("screenshot.png")
    try:
        main_slot = driver.find_element(By.CSS_SELECTOR, "div.s-main-slot")
        with open("main_slot.html", "w", encoding="utf-8") as f:
            f.write(main_slot.get_attribute("outerHTML"))
    except:
        print("❗ Could not dump main_slot HTML.")

    # Matching logic with fallback keywords
    keywords = ["ps5", "playstation 5", "sony ps5"]
    matches = [r.text for r in results if any(k in r.text.lower() for k in keywords)]

    # Debug output
    for i, r in enumerate(results):
        text = r.text.strip()
        print(f"[{i}] {text}")
        if any(k in text.lower() for k in keywords):
            print("✅ MATCH FOUND")

    assert matches, "❌ No product titles matched keywords"
