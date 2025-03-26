from base_page import BasePage
from my_page.my_locators import MyLocators


class MyMethods(MyLocators, BasePage):
    def open_request(self):
        self.find_element(locator=self.NEW_LOCATOR)
