from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def test_google_url(open_page):
    open_page.get("https://www.google.com")
    assert "google" in open_page.current_url
