# tests/test_searchAndApply.py
import pytest
from pages.login_page import LoginPage
from pages.search_page import SearchPage
from utils import config
from utils.logger import get_logger
logger = get_logger("test_searchAndApply")

@pytest.mark.parametrize("pages_to_apply", [config.PAGES_TO_APPLY])
def test_profile_navigation(driver, pages_to_apply):

    # Step 1: Login
    login_page = LoginPage(driver)
    login_page.login()
    logger.info("✅ Logged in successfully")

    # Step 2: Search for matching positions
    search_page = SearchPage(driver)
    search_page.Search_Matching_Postion()
    logger.info("🔍 Search executed successfully")

    # Step 3: Apply jobs across multiple pages
    search_page.ApplyPages(pages_to_apply)

    # Step 4: Print final summary
    logger.info("\n📊 Final Summary:")
    logger.info(f"Total jobs found across {pages_to_apply} pages: {search_page.total_notifications}")
    logger.info(f"Total jobs tried to apply: {search_page.tried_for_apply_job_count}")
    logger.info(f"Total jobs successfully applied: {search_page.applied_count}")

    # Step 5: Assertions
    assert search_page.total_notifications > 0, "❌ No jobs found to apply."
    assert search_page.tried_for_apply_job_count > 0, "❌ No jobs were attempted for apply."
    assert search_page.applied_count > 0, "❌ No jobs were applied successfully. Check ApplySearch or ClickDirectApply logic."
    logger.info(f"✅ Test passed: {search_page.applied_count} jobs applied successfully.")
