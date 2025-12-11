# utils/driver_setup.py
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_driver():
    username = os.getenv("BROWSERSTACK_USERNAME")
    access_key = os.getenv("BROWSERSTACK_ACCESS_KEY")

    options = Options()

    # Add BrowserStack capabilities inside ChromeOptions
    bstack_options = {
        "os": "Windows",
        "osVersion": "11",
        "sessionName": "Naukri Automation CI Run",
        "local": "false"
    }

    options.set_capability("bstack:options", bstack_options)
    options.set_capability("browserName", "Chrome")
    options.set_capability("browserVersion", "latest")

    driver = webdriver.Remote(
        command_executor=f"https://{username}:{access_key}@hub.browserstack.com/wd/hub",
        options=options
    )

    driver.maximize_window()
    return driver
