import time

class MotorProcessor:
    """Class for manage strategy."""

    def __init__(self, strategy, url) -> None:
        self.strategy = strategy
        self.search_motor = url

    def search_job(self) -> None:
        """Search joob in strategy selected"""
        return self.strategy.find_job(url=self.search_motor)
        # self.strategy.create_excel(cards)
        # self.strategy.customize_excel()
        # self.strategy.close_browser()
        # return "Ya se ha encontrado jale pa"

    def create_excel(self, cards) -> None:
        """Search joob in strategy selected"""
        return self.strategy.create_excel(cards)


    def customize_excel(self, cards) -> None:
        """Search joob in strategy selected"""
        self.strategy.customize_excel(element=cards)


    def close_browser(self) -> None:
        """Search joob in strategy selected"""
        self.strategy.close_browser()
