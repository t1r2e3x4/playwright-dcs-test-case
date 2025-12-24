from src.dog_cat_star import DogCatStar
from pages.product_page_helper import ProductPageHelper
from pages.cat_product_page import CatProductPage
from pages.dog_product_page import DogProductPage
from pages.login_page import LoginPage


def test_add_to_cart(logged_in_page):
    DogProductPage(logged_in_page).goto()
    helper = ProductPageHelper(logged_in_page)
    helper.add_product_to_cart_with_options(
        product_name="寵物濕巾｜濕式衛生紙&隨身包",
        options={"選擇規格": "大包46抽", "選擇商品": "單包"},
        max_pages=3,
    )
