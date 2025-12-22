from pages.base_page import BasePage

class CatProductPage(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = '/product-category/cat/'
    
    