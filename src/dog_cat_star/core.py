import logging
import os
from typing import Literal, Any, Dict, List

from playwright.sync_api import sync_playwright, Browser, Page, BrowserContext
from pages.login_page import LoginPage
from pages.index_page import IndexPage

logger = logging.getLogger(__name__)


class DogCatStar:
    def __init__(
        self,
        user_email: str = "",
        user_phone: str = "",
        base_url: str = "https://www.dogcatstar.com/",
        browser: Literal["chrome", "firefox"] = "chrome",
    ):
        self.base_url = base_url

        _lang = os.getenv("DOGCATSTAR_LANG", "zh-tw")
        self._playwright = sync_playwright().start()

        # Default to Chromium for 'chrome' option
        if browser == "chrome":
            bw = self._playwright.chromium
        else:
            bw = self._playwright.firefox

        self._browser = bw.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--ignore-certificate-errors",
            ],
        )

        user_agent = (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        self._context = self._browser.new_context(
            ignore_https_errors=True,
            # user_agent=user_agent,
            locale=_lang,
            # viewport={"width": 1920, "height": 1080},
        )
        # self._page = self._context.new_page()

    def close(self):
        self.__exit__(None, None, None)

    def __exit__(self, exc_type, exc_value, traceback):
        if self._context:
            self._context.close()
            self._context = None

        if self._browser:
            self._browser.close()
            self._browser = None

        if self._playwright:
            self._playwright.stop()
            self._playwright = None

        return False

    def open_homepage(self):
        logger.info(f"Opening homepage at {self.base_url}")
        page = self._context.new_page()
        index_page = IndexPage(page)
        return index_page.goto()
