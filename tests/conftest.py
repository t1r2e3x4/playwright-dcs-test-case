import pytest
from dotenv import load_dotenv
from src.dog_cat_star import DogCatStar

# 自動載入環境變數
@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()

@pytest.fixture(scope="function")
def dcs():
    """初始化 DogCatStar 應用程式物件，並在測試後關閉"""
    app = DogCatStar()
    yield app
    app.close()

@pytest.fixture(scope="function")
def page(dcs):
    """
    從 dcs 實例中取得一個新的 page。
    假設 dcs._context 已經初始化。
    """
    new_page = dcs._context.new_page()
    yield new_page
    new_page.close()
