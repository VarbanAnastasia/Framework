
from my_page.my_methods import MyMethods


class TestTestik:

    def test_testik(self, open_page):
        driver = open_page
        page = MyMethods(driver=driver)
        page.open_request()
