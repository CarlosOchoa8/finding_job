"""Browser Config class module"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class BrowserConfig:
    """Class to config Browser """

    # def __init__(self, service_manager, browser_options, broser_arguments: str | None = None) -> None:
    #     self.service_manager = service_manager
    #     self.browser_options = browser_options
    #     self.browser_arguments = broser_arguments


    # def create_browser(self):
    #     """Create browser. TODO to try another browser nor only chrome"""
    #     return webdriver.Chrome(  # type: ignore
    #         options=self.browser_options, service=self.service_manager
    #     )
    
    def create_browser(self):
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        browser = webdriver.Chrome(options=options, service=service)
        return browser
