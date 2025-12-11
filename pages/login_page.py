from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import config
from selenium.webdriver.common.alert import Alert
import time
from utils.logger import get_logger

logger = get_logger(__name__)

class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, by, value, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def wait_until_clickable(self, by, value, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )

    def login(self):
        self.driver.get(config.BASE_URL)
        logger.info(f"Page Title: {self.driver.title}")

        # Wait for page load
        WebDriverWait(self.driver, 30).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        # Retry finding login button up to 3 times
        for attempt in range(3):
            try:
                login_btn = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "login_Layer"))
                )
                login_btn.click()
                break
            except:
                logger.warning(f"Login button not found. Retry {attempt + 1}/3")
                time.sleep(2)
        else:
            raise Exception("Login button not clickable after retries")

        # Wait for login modal
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//input[@placeholder='Enter your active Email ID / Username']"))
        )
