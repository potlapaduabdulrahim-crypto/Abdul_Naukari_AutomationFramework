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
        logger.info(f"Navigated to {config.BASE_URL}")
        logger.info(f"Page Title: {self.driver.title}")
        time.sleep(5)
        try:
            self.wait_until_clickable(By.ID, "login_Layer").click()
            logger.info("Clicked on Login button")
            time.sleep(2)
            self.wait_for_element(By.XPATH, '//*[@id="root"]/div[4]/div[2]/div/div')
            logger.info("Login modal is visible")
            self.wait_for_element(By.XPATH, "//input[@placeholder='Enter your active Email ID / Username']").click()
            self.wait_for_element(By.XPATH, "//input[@placeholder='Enter your active Email ID / Username']").send_keys(config.USERNAME)
            time.sleep(2)
            logger.info("Username Entered Successfully.... ")

            self.wait_for_element(By.XPATH, "//input[@placeholder='Enter your password']").click()
            self.wait_for_element(By.XPATH, "//input[@placeholder='Enter your password']").send_keys(config.PASSWORD)
            time.sleep(2)
            logger.info("Username Entered Successfully....")

            self.wait_until_clickable(By.XPATH, "//button[text()='Login']").click()

            time.sleep(8)
            logger.info("Submitted login form")

        except Exception as e:
            logger.error(f"Login failed: {e}")
            raise
