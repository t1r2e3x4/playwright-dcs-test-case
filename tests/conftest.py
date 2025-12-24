import pytest
from pages.login_page import LoginPage
from pages.index_page import IndexPage
from src.dog_cat_star import DogCatStar


@pytest.fixture(scope="session")
def dog_cat_star():
    """
    建立 DogCatStar instance，整個 session 共用
    """
    client = DogCatStar(browser="chrome")
    yield client
    client.close()


@pytest.fixture(scope="function")
def page(dog_cat_star: DogCatStar):
    """
    每個 test function 都提供一個乾淨 page
    """
    page = dog_cat_star._context.new_page()
    index_page = IndexPage(page)
    index_page.goto()
    yield page


@pytest.fixture(scope="function")
def logged_in_page(dog_cat_star: DogCatStar):
    """
    每個 test 用 storage_state 建立已登入 page
    """
    context = dog_cat_star._browser.new_context(
        storage_state="./state_storage/state.json"
    )
    page = context.new_page()
    index_page = IndexPage(page)
    index_page.goto()
    yield page
    context.close()
