from pages.login_page import LoginPage
from src.dog_cat_star import DogCatStar
from helper.mail_otp.mail_otp import get_latest_otp_email
from dotenv import load_dotenv
import os
import time

def test_email_login(page):
    load_dotenv()
    EMAIL_ADDRESS = os.getenv("EMAIL_IMAP_USERNAME")
    login_page = LoginPage(page)
    login_page.goto()
    login_page.email_login(EMAIL_ADDRESS)
    
    retry = 0
    while True:
        otp_pass = get_latest_otp_email("汪喵星球")
        if otp_pass:
            break
        retry += 1
        if retry >= 10:
            print("Failed to get OTP email after several retries.")
            return
        time.sleep(3)
        print("OTP email not found yet, retrying...")
        
    login_page.enter_otp_password(otp_pass)