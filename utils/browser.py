import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# from time import sleep


DRIVER_DIR = Path(__file__).parent.parent
CHROMEDRIVER_NAME = "chromedriver"
CHROMEDRIVER_PATH = str(DRIVER_DIR / "bin" / CHROMEDRIVER_NAME)


def make_chrome_browser(*options):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--remote-debugging-port=9222")
    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    if os.environ.get("SELENIUM_HEADLESS") == "True":
        chrome_options.add_argument("--headless")

    chrome_service = Service(executable_path=CHROMEDRIVER_PATH)
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return browser


if __name__ == "__main__":
    browser = make_chrome_browser(
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--headless",
    )
    browser.get("http:/www.google.com.br/")
    browser.quit()
