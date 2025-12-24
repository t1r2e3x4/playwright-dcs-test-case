from urllib.parse import urljoin
from playwright.sync_api import Page


class BasePage:
    def __init__(
        self, page: Page, base_url: str = "https://www.dogcatstar.com/", *args, **kwargs
    ):
        self.page = page
        self.base_url = base_url
        self.path = ""
        super().__init__(*args, **kwargs)

    def goto_path(self, path: str):
        return self.page.goto(urljoin(self.base_url, path))

    @property
    def current_url(self):
        return self.page.url

    @property
    def is_in_current_page(self):
        return self.path in self.page.url
    
    @property
    def account_li(self):
        return self.page.locator("li.account-item:has(img[alt='User'])")

    @property
    def cart_li(self):
        return self.page.locator("li.cart-item:has(img[alt='Cart'])")
    
    #TODO: change locator to match better if needed
    @property
    def cart_count_a(self):
        return self.cart_li.locator(f"div:not(.header-button) > a[href*='cart']").first

    @property
    def num_items_in_cart(self) -> int:
        if self.cart_count_a.count() == 0:
            return 0
        else:
            count_text = self.cart_count_a.inner_text().strip()
            try:
                return int(count_text)
            except ValueError:
                return 0
            
    def goto(self):
        if not self.is_in_current_page:
            self.goto_path(self.path)
        else:
            return
