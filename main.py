from pages.index_page import IndexPage
from src.dog_cat_star import DogCatStar
from pages.login_page import LoginPage
from pages.dog_product_page import DogProductPage
from pages.product_page_helper import ProductPageHelper
from playwright.sync_api import Locator, Page, expect
from helper.mail_otp.mail_otp import get_latest_otp_email
import time
import json
import os
from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()
    # otp_pass = get_latest_otp_email("汪喵星球")
    # print(otp_pass)
    # dcs = DogCatStar()
    # context = dcs._browser.new_context(storage_state="./state_storage/state.json")

    # page = context.new_page()
    # login_page = LoginPage(page)
    # login_page.goto()
    # breakpoint()
    dcs = DogCatStar()
    page = dcs._context.new_page()
    dog_product_page = DogProductPage(page)
    dog_product_page.goto()
    print(dog_product_page.num_items_in_cart)

    helper = ProductPageHelper(page)
    helper.add_product_to_cart_with_options(
        product_name="寵物濕巾｜濕式衛生紙&隨身包",
        options={"選擇規格": "大包46抽", "選擇商品": "單包"},
        max_pages=3,
    )

    print(dog_product_page.num_items_in_cart)
    helper.add_product_to_cart_with_options(
        product_name="寵物濕巾｜濕式衛生紙&隨身包",
        options={"選擇規格": "大包46抽", "選擇商品": "單包"},
        max_pages=3,
    )
    print(dog_product_page.num_items_in_cart)
    breakpoint()
    # dcs.open_homepage()
    # # time.sleep(150)
    # # login_page = LoginPage(dcs._page)
    # # login_page.email_login(os.getenv("EMAIL_IMAP_USERNAME"))

    # dog_product_page = DogProductPage(dcs._page)
    # dog_product_page.goto()

    # helper = ProductPageHelper(dcs._page)
    # helper.add_product_to_cart_with_options(
    #     product_name="寵物濕巾｜濕式衛生紙&隨身包",
    #     options={
    #         "選擇規格": "大包46抽",
    #         "選擇商品": "單包"
    #     },
    #     max_pages=3
    # )

    # dog_product_page.product_add_to_cart_btn("汪喵星球 無膠純肉泥").click()
    # expect(dog_product_page.product_dialog("汪喵星球 無膠純肉泥")).to_be_visible()
    # d_option_test = dog_product_page.options_in_option_div("選擇規格")
    # # expect(d_option_test).to_be_visible()
    # print(d_option_test.count())
    # print(d_option_test.all_inner_texts())

    # dog_product_page.option_btn("口味", "雞肉").click()
    # dog_product_page.dialog_add_to_cart_button.click()
    # breakpoint()

    # dcs.driver.get("https://www.dogcatstar.com/my-account/")
    # time.sleep(150)
    # cookies = dcs.driver.get_cookies()

    # # 存成 json
    # with open("./cookies.json", "w", encoding="utf-8") as f:
    #     json.dump(cookies, f, ensure_ascii=False, indent=2)

    # dcs.driver.quit()

    # dcs = DogCatStar()
    # dcs.open_homepage()
    # for cookie in cookies:
    #     # Selenium 不接受 sameSite=None
    #     cookie.pop("sameSite", None)
    #     dcs.driver.add_cookie(cookie)
    # dcs.driver.refresh()
