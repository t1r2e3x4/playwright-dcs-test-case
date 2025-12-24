from src.dog_cat_star import DogCatStar
from pages.login_page import LoginPage
import os
from dotenv import load_dotenv
from helper.mail_otp.mail_otp import get_latest_otp_email
import time

load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_IMAP_USERNAME")


def main():
    dcs = DogCatStar()
    page = dcs._context.new_page()
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

    # TODO: wait for login to complete, use proper wait method
    time.sleep(5)
    dcs._context.storage_state(path="./state_storage/state.json")
    dcs.close()


if __name__ == "__main__":
    main()
