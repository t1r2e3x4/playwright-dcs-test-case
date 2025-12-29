import pytest
from dotenv import load_dotenv
import os
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

@pytest.fixture(scope="function")
def logged_in_page(dcs: DogCatStar):
    """
    嘗試載入登入狀態 (state.json) 的頁面。
    如果檔案存在，則直接以登入狀態啟動；否則開啟一般頁面。
    """
    state_path = "./state_storage/state.json"
    if os.path.exists(state_path):
        # 使用 dcs._browser 建立一個帶有 storage_state 的新 context
        context = dcs._browser.new_context(storage_state=state_path)
    else:
        context = dcs._browser.new_context()
    
    page = context.new_page()
    yield page
    context.close()
