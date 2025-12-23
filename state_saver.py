from src.dog_cat_star import DogCatStar
from pages.login_page import LoginPage
import os
from dotenv import load_dotenv
from helper.mail_otp.mail_otp import get_latest_otp_email
load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_IMAP_USERNAME")

def main():
    dcs = DogCatStar()
    dcs.open_homepage()
    login_page = LoginPage(dcs._page)
    login_page.goto()
    login_page.email_login(EMAIL_ADDRESS)
    
    retry = 0
    while True:
        otp_pass = get_latest_otp_email("汪喵星球")
        if otp_pass:
            break
        retry += 1
        if retry >= 5:
            print("Failed to get OTP email after several retries.")
            return
        print("OTP email not found yet, retrying...")

    dcs._context.storage_state(path="./state_storage/state.json")
    dcs._browser.close()
    
if __name__ == "__main__":
    main()