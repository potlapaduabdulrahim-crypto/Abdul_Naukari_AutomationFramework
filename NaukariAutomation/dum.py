import pandas as pd

pd.DataFrame















# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from utils import config
# from selenium.webdriver.common.alert import Alert
# import time
# from utils.logger import get_logger
# from selenium import webdriver
#
#
# driver = webdriver.Chrome()
# driver.maximize_window()
# driver.get("https://www.amazon.in/")
# # if driver.find_element(By.PARTIAL_LINK_TEXT,"Continue Shopping"):
# #     driver.find_element(By.LINK_TEXT,"Continue Shopping").click()
# # else:
# time.sleep(2)
# searchbar=driver.find_element(By.XPATH, "//input[@id='twotabsearchtextbox']")
# searchbar.send_keys("TV")
# time.sleep(2)
#
# driver.find_element(By.XPATH,'//*[@id="nav-search-submit-button"]').click()
# time.sleep(2)
# selectTV=driver.find_element(By.XPATH, "(//a[@class='a-link-normal s-line-clamp-2 s-line-clamp-3-for-col-12 s-link-style a-text-normal'])[1]").click()
# # driver.execute_script("arguments[0].scrollIntoView(true);", selectTV)
#
# driver.switch_to.window(driver.window_handles[1])
# time.sleep(2)
#
# addToCart=driver.find_element(By.XPATH,"//div[@class='a-section a-spacing-none a-padding-none']//input[@id='add-to-cart-button']")
# time.sleep(2)


# import re
# from playwright.sync_api import Playwright, sync_playwright, expect
#
#
# def run(playwright: Playwright) -> None:
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context()
#     page = context.new_page()
#     page.goto("https://www.amazon.in/")
#     page.get_by_role("searchbox", name="Search Amazon.in").click()
#     page.get_by_role("searchbox", name="Search Amazon.in").fill("tv")
#     page.get_by_role("searchbox", name="Search Amazon.in").press("Enter")
#     page.get_by_role("button", name="Go", exact=True).click()
#     with page.expect_popup() as page1_info:
#         page.get_by_role("link", name="Sponsored Ad - acer 108 cm (").click()
#     page1 = page1_info.value
#     page1.goto("https://www.amazon.in/acer-inches-Ultra-Google-AR43QDVGU2875BD/dp/B0FLKHQCDW/ref=sr_1_1_sspa?crid=2TUNW0FMIYU7U&dib=eyJ2IjoiMSJ9.eCn6eAvuqTHVgFbRQKjR_Lq734tT1zmVEuWXfRUBd779O5BK6rnZgLH56nA5kMFT99WEJ7N5ngqnlkegBzTd7nGoafDQzZ4WJ8JJy3cdpQ6ldY4IpqLe0OF9WEyI_byryxHwvxjKD-eeQ9utraHbJM_Dc96BG_mM7vtP0B4QzDOtoT1YKgyc4JQYP7YphhNwywz42l2G77rCzT2WzqSoiTqqOzr_m0sKVix7eb2aRtU.fuDOzf6BqFVPGpbvFoTgu4RcSkdvIU0zQEQ0UYFwgY0&dib_tag=se&keywords=tv&qid=1764934270&sprefix=tv%2Caps%2C249&sr=8-1-spons&aref=iRsqAwvv63&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1")
#     page1.get_by_role("button", name="Add to Cart").click()
#     page1.get_by_role("button", name="Proceed to Buy (2 items) Buy").click()
#
#     # ---------------------
#     context.close()
#     browser.close()
#
#
# with sync_playwright() as playwright:
#     run(playwright)

# addToCart.click()
# checkout=driver.find_element(By.XPATH,"//input[@name='proceedToRetailCheckout']")
# time.sleep(10)
#
# checkout.click()




# def get_answer_from_resume(question: str, resume_data: dict):
#     q = question.lower()
#
#     # Basic keyword matching logic
#     if "name" in q:
#         return resume_data.get("name")
#     elif "email" in q:
#         return resume_data.get("email")
#     elif "phone" in q or "mobile" in q:
#         return resume_data.get("phone")
#     elif "experience" in q or "years" in q:
#         return resume_data.get("experience")
#     elif "skill" in q or "technology" in q or "tech stack" in q:
#         return resume_data.get("skills")
#     elif "location" in q or "city" in q:
#         return resume_data.get("location")
#     elif "notice" in q:
#         return resume_data.get("notice_period")
#     elif "current" in q and "company" in q:
#         return "Honeywell"  # Optional
#     elif "expected" in q and "salary" in q:
#         return "As per company standards"
#     elif "relocate" in q or "relocation" in q:
#         return "Yes"
#     elif "willing" in q and "shift" in q:
#         return "Yes"
#     elif "python" in q:
#         return "Yes, I have hands-on experience with Python automation."
#     else:
#         return None
