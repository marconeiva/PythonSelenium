import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_search_ps5_on_amazon(driver):
    driver.get("https://www.amazon.com/")
    search_box = driver.find_element(By.ID, "twotabsearchtextbox")
    search_box.send_keys("ps5 console")
    search_box.send_keys(Keys.RETURN)

    results = driver.find_elements(By.CSS_SELECTOR, "span.a-text-normal")
    assert any("ps5" in result.text.lower() for result in results), "No PS5-related results found!"
