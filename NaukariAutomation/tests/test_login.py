from pages.login_page import LoginPage

def test_login(driver):
    login = LoginPage(driver)
    login.login()
    assert "Home | Mynaukri" in driver.title
