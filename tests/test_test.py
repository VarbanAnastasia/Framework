from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def test_open_google():
    options = Options()
    options.set_capability("browserName", "chrome")
    options.set_capability("version", "119.0")
    options.set_capability("enableVNC", True)

    driver = webdriver.Remote(
        command_executor="http://localhost:4444/wd/hub",
        options=options
    )

    driver.get("https://www.google.com")
    assert "Google" in driver.title
    driver.quit()
