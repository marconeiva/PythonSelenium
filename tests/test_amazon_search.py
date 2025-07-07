import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1920, 1080)
    yield driver
    driver.quit()


def test_search_ps5_on_amazon(driver):
    driver.get("https://www.amazon.com/")

    # Wait for the search box to be present
    wait = WebDriverWait(driver, 15)
    search_box = wait.until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))

    search_box.send_keys("ps5 console")
    search_box.send_keys(Keys.RETURN)

    results = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.a-text-normal"))
    )

    assert any("ps5" in result.text.lower() for result in results), "No PS5-related results found!"
