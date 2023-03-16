from pathlib import Path
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

DRIVER_DIR = Path(__file__).parent.parent
CHROMEDRIVER_NAME = "chromedriver"
CHROMEDRIVER_PATH = str(DRIVER_DIR / "bin" / CHROMEDRIVER_NAME)


def make_chrome_browser(*options):
    chrome_options = webdriver.ChromeOptions()
    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    chrome_service = Service(executable_path=CHROMEDRIVER_PATH)
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return browser


if __name__ == "__main__":
    browser = make_chrome_browser(
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--headless",
        "--remote-debugging-port=9222",
    )
    browser.get("http:/www.google.com.br/")
    sleep(5)
    browser.quit()
