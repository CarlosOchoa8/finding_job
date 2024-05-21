"""Strategy module"""
from abc import ABC, abstractmethod
from strategy.browser_config import BrowserConfig

class SearchingMotor(ABC, BrowserConfig):
    """Strategy main class"""

    @abstractmethod
    def __init__(self, job_title: str, job_location: str):
        """params for job seeking."""


    @abstractmethod
    def get_browser(self, url: str):
        """get browser according url webpage"""
        # browser = self.create_browser()
        # return browser.get(url)


    @abstractmethod
    def close_browser(self):
        """close browser after seek browser use."""

    @abstractmethod
    def find_job(self, url: str):
        """search job in URL for browser."""


    @abstractmethod
    def create_excel(self, element):
        """Create excel with recopilated job posts"""


    @abstractmethod
    def customize_excel(self, excel):
        """customize excel according web compiled."""
