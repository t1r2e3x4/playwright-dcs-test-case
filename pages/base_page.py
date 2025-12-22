from urllib.parse import urljoin
from playwright.sync_api import Page


class BasePage:
    def __init__(
        self, page: Page, base_url: str = "https://www.dogcatstar.com/", *args, **kwargs
    ):
        self.page = page
        self.base_url = base_url
        self.path = ""

    def goto_path(self, path: str):
        return self.page.goto(urljoin(self.base_url, path))

    @property
    def current_url(self):
        return self.page.url

    @property
    def is_in_current_page(self):
        return self.path in self.page.url
