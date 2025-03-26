import pytest

from my_page.my_methods import MyMethods


class TestOpenRequest:
    @pytest.mark.usefixtures("driver")
    def test_open_request_success(self, open_page):
        driver = open_page
        page = MyMethods(driver=driver)
        page.open_request()