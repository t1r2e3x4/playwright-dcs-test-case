from src.dog_cat_star import DogCatStar
from pages.login_page import LoginPage
from pages.dog_product_page import DogProductPage
import time
import json
import os
from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()
    dcs = DogCatStar()
    dcs.open_homepage()
    # time.sleep(150)
    # login_page = LoginPage(dcs._page)
    # login_page.email_login(os.getenv("EMAIL_IMAP_USERNAME"))

    dog_product_page = DogProductPage(dcs._page)
    dog_product_page.goto()

    dog_product_page.product_add_to_cart_btn("迪士尼貓狗系列 WIDEN寬寬防漏碗").click()
    d_option_test = dog_product_page.options_in_option_div("款式")
    print(d_option_test.count())
    print(d_option_test.all_inner_texts())
    breakpoint()
    
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