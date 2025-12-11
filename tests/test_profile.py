from pages.login_page import LoginPage
from pages.profile_page import ProfilePage

def test_profile_navigation(driver):
    LoginPage(driver).login()
    ProfilePage(driver).navigate_to_View_profile()
    assert "Profile | Mynaukri" in driver.title
