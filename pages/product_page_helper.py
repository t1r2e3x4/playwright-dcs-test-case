from playwright.sync_api import expect, TimeoutError
from pages.base_page import BasePage
from pages.product_page_mixin import ProductPageMixin
import time
import logging

logger = logging.getLogger(__name__)
class ProductPageHelper(BasePage, ProductPageMixin):

    def add_product_to_cart_with_options(
        self,
        product_name: str,
        options: dict[str, str] = None,
        max_pages: int = 5
    ) -> bool:
        """
        從分頁找到商品，點擊加入購物車，選擇規格與口味，最後確認加入購物車。
        
        :param product_name: 商品名稱
        :param options: 選項字典，例如 {"選擇規格": "大包", "口味": "雞肉"}
        :param max_pages: 最多翻頁數
        :return: 是否成功加入購物車
        """
        for page_index in range(max_pages):
            # try to wait for page loading and product containers to be visible
            self.product_containers.first.wait_for(state="visible", timeout=5000)
            # 嘗試在當前頁面找到商品
            product_locator = self.product_container(product_name)
            
            if product_locator.count() > 0:
                # 點擊商品加入購物車按鈕
                add_btn = self.product_add_to_cart_btn(product_name)
                expect(add_btn).to_be_visible()
                expect(add_btn).to_be_enabled()
                
                # TODO: 有時候按太快會沒反應，暫時用 wait_for_load_state 解決，感覺是在等 API 回應？
                self.page.wait_for_load_state("load")
                add_btn.click()

                # 等待對話框出現
                dialog = self.product_dialog(product_name)
                expect(dialog).to_be_visible(timeout=5000)

                # 如果有 options，依序選擇
                if options:
                    for category, option_name in options.items():
                        try:
                            option_button = self.option_btn(category, option_name)
                            expect(option_button).to_be_visible()
                            if option_button.get_attribute("data-testid") == "selected":
                                continue  # 已選擇則跳過
                            else:
                                option_button.click()
                        except:
                            logger.error(f"無法選擇選項 {category} 的 {option_name}")
                            return False
                        
                # 最後點擊對話框加入購物車
                expect(self.dialog_add_to_cart_button).to_be_visible()
                expect(self.dialog_add_to_cart_button).to_be_enabled()
                self.dialog_add_to_cart_button.click()

                return True

            # 如果沒找到，檢查下一頁按鈕
            try:
                if self.pagination_next_btn.is_enabled():
                    self.pagination_next_btn.click()
                else:
                    break
            except TimeoutError:
                break

        return False
