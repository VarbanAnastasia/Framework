def test_open_google(browser):
    browser.get("https://www.google.com")
    assert "Google" in browser.title
