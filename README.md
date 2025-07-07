# 🧪 Sample project that does a PS5 Search Test at Amazon with (Selenium + Pytest + Docker + CI)

This project automates the validation of Amazon search functionality for the keyword **"ps5 console"** using:

- ✅ **Python 3.11**
- 🔍 **Selenium WebDriver** with headless **Chromium**
- 🧪 **Pytest** for test management and HTML reporting
- 🐳 **Docker** for cross-platform test execution
- 🔁 **Bitbucket Pipelines** for continuous integration

---

## 🔍 What It Does

The test script opens [amazon.com](https://www.amazon.com/-/en/), simulates a user searching for **PS5 console**, and verifies that relevant product titles appear in the results.

It handles:
- Location/cookie modals
- Headless scrolling for lazy-loaded items
- CAPTCHA detection (to flag bot blocks)
- Screenshot + HTML dump for CI artifacts

---


---

## 🚀 Getting Started Locally

### 1. Build and run in Docker

```bash
docker build -t selenium-test-image .
docker run --rm -v $(pwd):/tests -w /tests selenium-test-image


