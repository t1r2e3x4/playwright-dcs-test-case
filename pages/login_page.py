from .base_page import BasePage
from playwright.sync_api import Locator, expect


class LoginPage(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = "/my-account/"
        self.line_btn: Locator = self.page.locator("button:text('使用 LINE 帳號登入'")
        self.facebook_btn: Locator = self.page.locator(
            "button:text('使用 Facebook 帳號登入')"
        )
        self.google_btn: Locator = self.page.locator("button:text('使用 Google 帳號登入')")
        self.email_btn: Locator = self.page.locator("button:text('使用 Email 登入')")
        self.phone_national_code_dropdown: Locator = self.page.locator(
            "div.MuiBox-root > div.MuiFormControl-root"
        )
        self.phone_input: Locator = self.page.locator("input#billing_phone")
        
        
        # email login process locators
        self.email_login_container: Locator = self.page.locator("div:has(div>h4:text('使用 Email 登入'))")
        self.email_banner: Locator = self.email_login_container.locator("p:text('Email')")
        self.email_input: Locator = self.email_login_container.locator('input[name="email"]')
        self.email_submit_btn: Locator = self.email_login_container.locator("button:has-text('確認')")
        
    def click_email_login(self):
        self.email_btn.click()
        
    def enter_email(self, email: str):
        self.email_banner.wait_for(timeout=5000)
        self.email_input.fill(email)
        expect(self.email_submit_btn).to_be_visible()
        expect(self.email_submit_btn).to_be_enabled()
        self.email_submit_btn.click()
        
    def email_login(self, email: str):
        self.go_to_login()
        self.click_email_login()
        self.enter_email(email)
        input("完成 Email 登入後按 Enter")
        
        
    
        
    
