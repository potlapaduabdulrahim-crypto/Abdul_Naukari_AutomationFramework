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

        # --- Wait until the page is fully loaded ---
        WebDriverWait(self.driver, 30).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        logger.info("Page fully loaded.")

        # --- MULTI-LOCATOR LOGIN HANDLING FOR ALL NAUKRI UI VARIANTS ---
        locators = [
            (By.ID, "login_Layer"),  # OLD UI (India region)
            (By.XPATH, "//div[contains(text(),'Login')]"),  # NEW UI top login button
            (By.XPATH, "//a[contains(text(),'Login')]"),  # Dropdown link inside menu
            (By.XPATH, "//span[contains(text(),'Login')]"),  # Mobile/tablet UI
            (By.XPATH, "//button[contains(text(),'Login')]"),
            (By.XPATH,"(//a[normalize-space()='Login'])[1]"),
            (By.CSS_SELECTOR,"#login_Layer")
            # Sometimes a button
        ]

        clicked = False

        for locator in locators:
            try:
                logger.info(f"Trying login locator: {locator}")
                login_btn = WebDriverWait(self.driver, 12).until(
                    EC.element_to_be_clickable(locator)
                )
                login_btn.click()
                logger.info(f"Clicked login button using locator: {locator}")
                clicked = True
                break
            except Exception as e:
                logger.warning(f"Locator failed: {locator} | Error: {e}")

        if not clicked:
            raise Exception("❌ Could not find ANY login button on Naukri UI — UI variant mismatch.")

        # --- Wait for login modal to appear ---
        try:
            username_input = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//input[@placeholder='Enter your active Email ID / Username']")
                )
            )
            logger.info("Login modal visible.")
        except:
            raise Exception("❌ Login modal did NOT appear after clicking login button.")

        # --- Fill username ---
        username_input.clear()
        username_input.send_keys(config.USERNAME)
        logger.info("Username entered.")

        # --- Fill password ---
        password_input = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@placeholder='Enter your password']")
            )
        )
        password_input.clear()
        password_input.send_keys(config.PASSWORD)
        logger.info("Password entered.")

        # --- Click Login button inside modal ---
        login_submit = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Login']"))
        )
        login_submit.click()
        logger.info("Login button clicked inside modal.")

        # --- Wait after login ---
        time.sleep(5)
        logger.info(f"Final title after login attempt: {self.driver.title}")
