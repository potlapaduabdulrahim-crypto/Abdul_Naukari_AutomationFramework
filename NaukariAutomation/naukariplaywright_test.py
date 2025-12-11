import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.naukri.com/")
    page.get_by_role("link", name="Login", exact=True).click()
    page.get_by_role("textbox", name="Enter your active Email ID /").click()
    page.get_by_role("textbox", name="Enter your active Email ID /").fill("potlapaduabdulrahim@gmail.com")
    page.get_by_role("textbox", name="Enter your active Email ID /").press("Tab")
    page.get_by_role("textbox", name="Enter your password").press("CapsLock")
    page.get_by_role("textbox", name="Enter your password").fill("N")
    page.get_by_role("textbox", name="Enter your password").press("CapsLock")
    page.get_by_role("textbox", name="Enter your password").fill("Nafirahim#@240125")
    page.get_by_role("textbox", name="Enter your password").press("Enter")
    page.get_by_role("button", name="Login", exact=True).click()
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
