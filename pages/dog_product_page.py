from pages.base_page import BasePage
from pages.product_page_mixin import ProductPageMixin


class DogProductPage(BasePage, ProductPageMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = "/product-category/dog/"
