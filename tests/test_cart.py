from src.dog_cat_star import DogCatStar
from pages.product_page_helper import ProductPageHelper
from pages.cat_product_page import CatProductPage
from pages.dog_product_page import DogProductPage
from pages.login_page import LoginPage
import pytest

@pytest.mark.parametrize(
    "product_name,options",
    [
        ("寵物濕巾｜濕式衛生紙&隨身包", {"選擇規格": "大包46抽", "選擇商品": "單包"}),
        ("汪喵星球 排毛保健純肉泥｜保健肉泥", {"選擇包裝": "兩盒40包"}),
    ],
)
def test_add_dog_product_to_cart(page, product_name, options):
    dog_product_page = DogProductPage(page)
    dog_product_page.goto()
    prev_num_items = dog_product_page.num_items_in_cart
    helper = ProductPageHelper(page)
    add_to_cart_result = helper.add_product_to_cart_with_options(
        product_name=product_name,
        options=options,
        max_pages=3,
    )
    current_num_items = dog_product_page.num_items_in_cart

    assert add_to_cart_result, f"應該成功加入商品 {product_name} 到購物車"
    assert current_num_items == prev_num_items + 1, f"加入購物車後，購物車數量應該增加 1，之前是 {prev_num_items}，現在是 {current_num_items}"
    
    
@pytest.mark.parametrize(
    "product_name,options",
    [
        ("迪士尼貓狗系列 COZY 四季被", {"款式": "魯斯佛款"}),
        ("迪士尼貓狗系列 COZY 四季被", {"款式": "瑪麗貓款"}),
    ],
)
def test_add_cat_product_to_cart(page, product_name, options):
    cat_product_page = CatProductPage(page)
    cat_product_page.goto()
    prev_num_items = cat_product_page.num_items_in_cart
    helper = ProductPageHelper(page)
    add_to_cart_result = helper.add_product_to_cart_with_options(
        product_name=product_name,
        options=options,
        max_pages=3,
    )
    current_num_items = cat_product_page.num_items_in_cart

    assert add_to_cart_result, f"應該成功加入商品 {product_name} 到購物車"
    assert current_num_items == prev_num_items + 1, f"加入購物車後，購物車數量應該增加 1，之前是 {prev_num_items}，現在是 {current_num_items}"