import time
import json
from utils import config
from utils.logger import get_logger
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
    ElementClickInterceptedException,
    NoSuchElementException
)
from utils.AutoApplyUtils import get_answer_from_resume

logger = get_logger(__name__)

class SearchPage:
    def __init__(self, driver):
        self.driver = driver
        self.applied_count = 0
        self.tried_for_apply_job_count = 0
        self.total_notifications = 0

    def Search_Matching_Postion(self):
        wait = WebDriverWait(self.driver, 10)

        self.driver.find_element(By.XPATH, "//span[@class='nI-gNb-sb__placeholder']").click()
        time.sleep(2)

        skill_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Enter keyword / designation / companies']")))
        skill_input.click()
        skill_input.send_keys(config.SKILL_COMPANY_DESIGNATION)
        time.sleep(2)

        experience_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "experienceDD")))
        experience_dropdown.click()
        time.sleep(1)
        logger.info("Skill/Company/Designation Entered Successfully...")

        experience_value = int(float(config.EXPERIENCE_YEARS))
        for _ in range(experience_value):
            experience_dropdown.send_keys(Keys.DOWN)
            time.sleep(0.2)
        experience_dropdown.send_keys(Keys.ENTER)
        logger.info("Experience set Successfully...")
        time.sleep(2)

        location_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Enter location']")))
        location_input.click()
        location_input.send_keys(config.Location)
        time.sleep(2)
        logger.info("Entered Location Successfully...")

        search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Search']")))
        search_button.click()
        logger.info("Search Button Clicked Successfully...")
        time.sleep(5)

    def ApplySearch(self):
        wait = WebDriverWait(self.driver, 15)
        index = 0

        try:
            with open(config.RESUME_DATA, "r", encoding="utf-8") as f:
                resume_data = f.read()
        except Exception as e:
            logger.error(f"❌ Failed to load resume data: {e}")
            return

        try:
            job_container = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='styles_jlc__main__VdwtF']")))
        except TimeoutException:
            logger.info("❌ No job listings found.")
            return

        job_cards = job_container.find_elements(By.XPATH, "./div")
        page_notifications = len(job_cards)
        self.total_notifications += page_notifications
        logger.info(f"📢 Total loaded job cards on this page: {page_notifications}")

        while index < page_notifications:
            job_card = job_cards[index]
            self.driver.execute_script("arguments[0].scrollIntoView(true);", job_card)
            time.sleep(0.5)

            try:
                job_card.find_element(By.XPATH, ".//*[contains(text(), 'Filter jobs by')]")
                logger.info(f"⚠️ Skipping job #{index + 1} due to 'Filter jobs by'")
                index += 1
                continue
            except NoSuchElementException:
                pass

            try:
                job_card.click()
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", job_card)
            time.sleep(2)

            logger.info(f"🟢 Opened job #{index + 1}")
            self.tried_for_apply_job_count += 1

            self.driver.switch_to.window(self.driver.window_handles[-1])
            logger.info("👉 Switched to new job tab")

            result = self.ClickDirectApply()

            if result is True:
                logger.info(f"✅ Applied for job #{index + 1}")
            elif result == "Apply on company site":
                logger.info(f"⚠️ Skipped job #{index + 1}: Apply on company site")
            else:
                logger.info(f"❌ Failed to apply job #{index + 1}")

            try:
                popup_handled = self.handle_apply_popup(resume_data)
                if popup_handled:
                    logger.info("✅ Popup handled and submitted successfully")
                else:
                    logger.info("ℹ️ No popup appeared after apply click")
            except Exception as e:
                logger.warning(f"⚠️ Error while handling popup: {e}")

            time.sleep(1)
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            logger.info(f"⬅️ Returned to main tab\n")
            index += 1
            time.sleep(1)

    def ClickDirectApply(self):
        try:
            wait = WebDriverWait(self.driver, 5)

            company_site_button = self.driver.find_elements(By.XPATH, "//button[@id='company-site-button']")
            if company_site_button and "Apply on company site" in company_site_button[0].text.strip():
                logger.info("⚠️ Skipping: Apply on company site button found.")
                return "Apply on company site"

            apply_button = self.driver.find_elements(By.XPATH, "//button[@id='apply-button']")
            if apply_button:
                apply_button[0].click()
                logger.info("✅ Direct Apply button clicked successfully.")
                self.applied_count += 1
                return True
            else:
                logger.info("❌ No Apply button found.")
                return False

        except Exception as e:
            logger.error(f"❌ Exception in ClickDirectApply: {e}")
            return False

    def ApplyPages(self, page_count: int):
        wait = WebDriverWait(self.driver, 15)

        for page in range(page_count):
            logger.info(f"\n🔹 Processing page {page + 1} of {page_count}")
            self.ApplySearch()

            logger.info(f"📊 Page {page + 1} summary: Tried: {self.tried_for_apply_job_count}, Applied: {self.applied_count}")

            if page < page_count - 1:
                try:
                    next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Next']")))
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                    time.sleep(1)
                    try:
                        next_button.click()
                    except ElementClickInterceptedException:
                        self.driver.execute_script("arguments[0].click();", next_button)
                    logger.info(f"➡️ Navigated to page {page + 2}")
                    time.sleep(5)
                except TimeoutException:
                    logger.info("⚠️ No Next button found, stopping pagination.")
                    break
            else:
                logger.info("✅ Finished all requested pages.")

        logger.info(f"\n✅ Total jobs found: {self.total_notifications}")
        logger.info(f"📌 Total jobs tried to apply: {self.tried_for_apply_job_count}")
        logger.info(f"📌 Total jobs successfully applied: {self.applied_count}")

    def handle_apply_popup(self, resume_data, hidden_json=None):
        """
        Handles Naukri chatbot popup in conversational flow:
        - Answers one question at a time
        - Types into editable chat box
        - Clicks Save to submit
        - Waits for next question to appear
        """
        wait = WebDriverWait(self.driver, 10)

        try:
            popup = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "chatbot_MessageContainer")))
            logger.info("⚡ Chatbot popup detected")

            while True:
                try:
                    # Wait for the latest question to appear
                    question_element = wait.until(EC.presence_of_element_located(
                        (By.XPATH, "//li[contains(@class,'chatbot_ListItem')][last()]//span")))
                    question_text = question_element.text.strip()
                    logger.info(f"💬 New question: {question_text}")

                    # Generate answer using Hugging Face
                    answer = get_answer_from_resume(question_text, resume_data, hidden_json)
                    logger.info("Writing the answer:"+answer)
                    # Try yes/no button logic first
                    try:
                        yes_button = self.driver.find_element(By.XPATH, "//button[normalize-space()='Yes']")
                        no_button = self.driver.find_element(By.XPATH, "//button[normalize-space()='No']")
                        if "yes" in answer.lower():
                            yes_button.click()
                            logger.info("🟢 Clicked YES")
                            time.sleep(1)
                            continue
                        elif "no" in answer.lower():
                            no_button.click()
                            logger.info("🔴 Clicked NO")
                            time.sleep(1)
                            continue
                    except NoSuchElementException:
                        pass

                    # Type into editable chat box
                    try:
                        input_box = self.driver.find_element(By.XPATH,
                                                             "//div[contains(@id,'InputBox') and @contenteditable='true']")
                        input_box.click()
                        input_box.send_keys(answer)
                        time.sleep(3)
                        logger.info(f"✍️ Typed answer: {answer}")

                        # Click Save
                        save_button = self.driver.find_element(By.XPATH, "//div[contains(@class,'sendMsg')]")
                        save_button.click()
                        logger.info("📨 Saved response")
                        time.sleep(2)
                        continue
                    except Exception as e:
                        logger.warning(f"⚠️ Failed to type or save answer: {e}")
                        break

                except TimeoutException:
                    logger.info("✅ No more questions or popup closed")
                    break

            return True

        except TimeoutException:
            logger.info("ℹ️ No chatbot popup appeared")
            return False
