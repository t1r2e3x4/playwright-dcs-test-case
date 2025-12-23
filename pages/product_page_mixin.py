import re
from playwright.sync_api import Locator, Page, expect

class ProductPageMixin:
    page: Page
    
    @property
    def product_dialog_div(self) -> Locator:
        return self.page.locator("div[data-testid='dialog-paper']")
    
    @property
    def dialog_add_to_cart_button(self) -> Locator:
        return self.product_dialog_div.locator("button:text('加入購物車')")
    
    @property
    def pagination_div(self) -> Locator:
        return self.page.locator("div > nav.woocommerce-pagination")
    
    @property
    def pagination_next_btn(self) -> Locator:
        return self.pagination_div.locator("a.next.page-number")
    
    @property
    def pagination_prev_btn(self) -> Locator:
        return self.pagination_div.locator("a.prev.page-number")

    @property
    def product_containers(self) -> Locator:
        return self.page.locator("div.product-small")
    
    def product_container(self, product_name:str) -> Locator:
        return self.page.locator(f"div.product-small:has(a:text('{product_name}'))")
    
    def product_add_to_cart_btn(self, product_name:str) -> Locator:
        product_container = self.product_container(product_name)
        return product_container.locator("button:text('加入購物車')")
    
    def product_dialog(self, product_name:str) -> Locator:
        return self.page.locator(f"div[data-testid='dialog-paper']:has(h5:text('{product_name}'))")
    
    def option_div(self, option_category:str) -> Locator:
        option_heading = self.product_dialog_div.locator(f"h6:has-text('{option_category}')")
        return option_heading.locator("..")

    def options_in_option_div(self, option_category:str) -> Locator:
        option_div = self.option_div(option_category)
        return option_div.locator("div > button")

    def option_btn(self, option_category:str, option_name:str) -> Locator:
        return self.options_in_option_div(option_category).locator(f"p:text('{option_name}')").locator("..")