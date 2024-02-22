from abc import ABC, abstractmethod


class BaseCrawler(ABC):
    @abstractmethod
    def run_crawling(self, *args, **kwargs):
        pass
