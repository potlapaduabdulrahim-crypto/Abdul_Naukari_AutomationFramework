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
        # 1. Navigate to Naukri
        self.driver.get(config.BASE_URL)
        logger.info(f"Navigated to {config.BASE_URL}")
        logger.info(f"Page Title: {self.driver.title}")

        # 👇👇👇 ADD DEBUG BLOCK (VERY IMPORTANT for CI)
        logger.warning(f"PAGE TITLE IN CI: {self.driver.title}")
        try:
            html_snippet = self.driver.page_source[:300]
            logger.warning(f"PAGE HTML SNIPPET: {html_snippet}")
        except:
            logger.warning("Could not read page HTML")
        # 👆👆👆 DEBUG BLOCK ENDS HERE

        # 2. Handle Access Denied (CI / Headless block)
        if "Access Denied" in self.driver.title:
            logger.warning("⚠ Access Denied detected — retrying...")
            self.driver.delete_all_cookies()
            time.sleep(2)
            self.driver.get(config.BASE_URL)
            logger.info("Retried loading the page")
            time.sleep(3)

        # SAFETY: Check again
        if "Access Denied" in self.driver.title:
            raise Exception("❌ Still blocked by Access Denied — Selenium headless detected")

        try:
            # 3. Ensure page is fully ready
            WebDriverWait(self.driver, 20).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )

            logger.info(f"Final Page Title after reload: {self.driver.title}")

            # 4. Click Login button (with retry block)
            try:
                self.wait_until_clickable(By.ID, "login_Layer").click()
            except:
                logger.warning("login_Layer NOT FOUND — retrying page load...")
                self.driver.get(config.BASE_URL)
                time.sleep(3)
                logger.warning(f"RETRY PAGE TITLE: {self.driver.title}")
                logger.warning(f"RETRY HTML SNIPPET: {self.driver.page_source[:200]}")
                self.wait_until_clickable(By.ID, "login_Layer").click()

            logger.info("Clicked on Login button")

            # 5. Wait for login modal
            self.wait_for_element(By.XPATH, '//*[@id="root"]/div[4]/div[2]/div/div')
            logger.info("Login modal is visible")

            # 6. Enter Username
            user_input = self.wait_for_element(
                By.XPATH, "//input[@placeholder='Enter your active Email ID / Username']"
            )
            user_input.clear()
            user_input.send_keys(config.USERNAME)
            logger.info("Username entered")

            # 7. Enter Password
            pass_input = self.wait_for_element(
                By.XPATH, "//input[@placeholder='Enter your password']"
            )
            pass_input.clear()
            pass_input.send_keys(config.PASSWORD)
            logger.info("Password entered")

            # 8. Click Login
            self.wait_until_clickable(By.XPATH, "//button[text()='Login']").click()
            logger.info("Clicked Login button")

            time.sleep(5)
            logger.info("Login submitted")

        except Exception as e:
            logger.error(f"Login failed: {e}")
            raise
