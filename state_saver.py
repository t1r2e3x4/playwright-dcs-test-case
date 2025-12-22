from src.dog_cat_star import DogCatStar
from pages.login_page import LoginPage

def main():
    dcs = DogCatStar()
    dcs.open_homepage()
    login_page = LoginPage(dcs._page)
    login_page.go_to_login()
    input("登入完成後按 Enter")

    dcs._context.storage_state(path="./state_storage/state.json")
    dcs._browser.close()
    
if __name__ == "__main__":
    main()