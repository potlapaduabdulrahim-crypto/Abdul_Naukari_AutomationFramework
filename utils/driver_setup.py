import os
from selenium import webdriver

def get_driver():
    username = os.getenv("BROWSERSTACK_USERNAME")
    access_key = os.getenv("BROWSERSTACK_ACCESS_KEY")

    capabilities = {
        "browserName": "Chrome",
        "browserVersion": "latest",
        "bstack:options": {
            "os": "Windows",
            "osVersion": "11",
            "local": "false",
            "seleniumVersion": "4.21.0",
            "sessionName": "Naukri Automation CI Run"
        }
    }

    driver = webdriver.Remote(
        command_executor=f"https://{username}:{access_key}@hub.browserstack.com/wd/hub",
        options=webdriver.ChromeOptions(),
        desired_capabilities=capabilities
    )

    driver.maximize_window()
    return driver
