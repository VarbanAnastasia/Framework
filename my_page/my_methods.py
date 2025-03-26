from base_page import BasePage
from my_page.my_locators import MyLocators


class MyMethods(MyLocators, BasePage):
    def __init__(self, driver):
        BasePage.__init__(self, driver=driver)

    def open_request(self):
        self.find_element(locator=self.NEW_LOCATOR)
