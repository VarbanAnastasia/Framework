import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import allure

@pytest.fixture
def browser(request):
    options = Options()
    options.add_argument('--start-maximized')
    driver = webdriver.Remote(
        command_executor='http://selenoid:4444/wd/hub',
        options=options
    )
    yield driver

    if request.node.rep_call.failed:
        allure.attach(driver.get_screenshot_as_png(),
                      name="screenshot",
                      attachment_type=allure.attachment_type.PNG)
    driver.quit()

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
