import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.usefixtures("driver")
def test_search_ps5_on_amazon(driver):
    driver.get("https://www.amazon.com/-/en/")

    wait = WebDriverWait(driver, 20)

    # Force US locale via cookie (must be set after first load)
    driver.add_cookie({"name": "lc-main", "value": "en_US"})
    driver.refresh()

    # Handle location modal (e.g., zip popup)
    try:
        wait.until(EC.element_to_be_clickable((By.ID, "nav-global-location-popover-link"))).click()
        time.sleep(1)
    except:
        pass  # Often doesn't appear in headless mode

    # Dismiss cookies if present
    try:
        cookie_btn = wait.until(EC.element_to_be_clickable((By.ID, "sp-cc-accept")))
        cookie_btn.click()
    except:
        pass

    # Wait and interact with the search bar
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "twotabsearchtextbox")))
    driver.execute_script("arguments[0].scrollIntoView(true);", search_box)
    driver.execute_script("arguments[0].focus();", search_box)
    time.sleep(1)

    # Dismiss any popups/overlays
    try:
        driver.switch_to.active_element.send_keys(Keys.ESCAPE)
        time.sleep(1)
    except:
        pass

    # Perform search
    search_box.clear()
    search_box.send_keys("ps5 console")
    search_box.send_keys(Keys.RETURN)

    # Wait for results to load
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-main-slot")))

    # Scroll down to load lazy-loaded content
    for _ in range(3):
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        time.sleep(1.5)

    # Save page source for debug
    driver.save_screenshot("screenshot.png")
    with open("main_slot.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    # CAPTCHA detection
    if "Enter the characters you see below" in driver.page_source:
        raise Exception("❗ CAPTCHA page detected. Amazon blocked the bot.")

    # Extract product titles
    results = driver.find_elements(By.CSS_SELECTOR, "h2 span.a-text-normal")

    # Match product titles
    keywords = ["ps5", "playstation 5", "sony ps5"]
    matches = [r.text for r in results if any(k in r.text.lower() for k in keywords)]

    # Debug logging
    for i, r in enumerate(results):
        text = r.text.strip()
        print(f"[{i}] {text}")
        if any(k in text.lower() for k in keywords):
            print("✅ MATCH FOUND")

    # Final assertion
    assert matches, "❌ No matching PS5 results found"
