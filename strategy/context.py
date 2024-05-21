import time

class MotorProcessor:
    """Class for manage strategy."""

    def __init__(self, strategy, url) -> None:
        self.strategy = strategy
        self.search_motor = url

    def search_job(self) -> None:
        """Search joob in strategy selected"""
        return self.strategy.find_job(url=self.search_motor)


    def create_excel(self, cards) -> None:
        """Search joob in strategy selected"""
        NotImplemented


    def customize_excel(self, cards) -> None:
        """Search joob in strategy selected"""
        self.strategy.customize_excel(element=cards)


    def close_browser(self) -> None:
        """Search joob in strategy selected"""
        self.strategy.close_browser()
