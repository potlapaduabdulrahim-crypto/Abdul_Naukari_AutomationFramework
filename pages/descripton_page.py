from selenium.webdriver.common.by import By

class DescriptionPage:
    def __init__(self, driver):
        self.driver = driver

    def update_description(self, new_text):
        self.driver.find_element(By.XPATH, "//span[text()='Description']").click()
        textarea = self.driver.find_element(By.XPATH, "//textarea[@name='description']")
        textarea.clear()
        textarea.send_keys(new_text)
        self.driver.find_element(By.XPATH, "//button[text()='Save']").click()
