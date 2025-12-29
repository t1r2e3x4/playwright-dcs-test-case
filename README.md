## 環境安裝與測試執行

1) 建議建立並啟用 virtualenv（選擇性，但推薦）

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2) 安裝 Python 相依套件（會使用專案根目錄的 `requirement.txt`）

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirement.txt
```

3) 安裝 Playwright 的瀏覽器二進位檔（必要，否則 Playwright 無法啟動瀏覽器）

```bash
python3 -m playwright install
```

4) 依照 .env.example 新增 .env 檔案，主要是用在自動使用 email 登入，並在初次執行的時候跑過 state_saver.py

```bash
python3 state_saver.py
```

5) 執行所有 pytest 測試

```bash
pytest -q
```

## TestCase
### 會員登入流程測試
| 測試案例                       | 期望結果              |
| -------------------------- | ----------------- |
| 使用正確帳號密碼登入                 | 登入成功，導向會員首頁或商品頁   |
| 使用錯誤密碼登入                   | 登入失敗，提示「密碼錯誤」     |
| 使用不存在帳號登入                  | 登入失敗，提示「帳號不存在」    |
| 空帳號或空密碼登入                  | 登入失敗，提示「請輸入帳號/密碼」 |
| 登入後保持登入狀態 (Cookie/Session) | 關閉瀏覽器後再開啟，仍保持登入   |
| 登入後登出                      | 成功登出，導向首頁或登入頁     |

### 商品加入購物車流程測試
| 測試案例            | 期望結果               |
| --------------- | ------------------ |
| 登入後將單一商品加入購物車   | 商品成功加入購物車，購物車數量增加  |
| 登入後將同一商品加入購物車多次 | 商品數量累加，金額正確計算      |
| 登入後將多個不同商品加入購物車 | 所有商品正確顯示於購物車       |
| 登入後加入庫存不足商品     | 提示「登入提醒」或加入失敗      |
| 登入後從商品頁加入購物車    | 購物車更新正確，頁面可正常跳轉或提示 |
| 登入後從商品列表頁加入購物車  | 購物車更新正確，頁面保持列表頁    |

### 邊界條件/異常流程
| 測試案例                 | 期望結果         |
| -------------------- | ------------ |
| 未登入直接加入商品購物車         | 應要可以使用訪客加入購物車 |
| 同時多個分頁操作購物車          | 購物車數量及內容同步正確 |
| 登入後網路斷線再加入商品         | 提示操作失敗，可重試   |
| 商品加入購物車後立即結帳         | 商品資料正確帶入結帳頁面 |

### UI / 可用性檢查
| 測試案例          | 期望結果                 |
| ------------- | -------------------- |
| 加入購物車按鈕點擊後有反饋 | 顯示「已加入購物車」提示或動畫      |
| 購物車數量即時更新     | 加入商品後購物車 icon 顯示正確數量 |
| 登入成功後頁面元素正確顯示 | 顯示會員名稱、登出按鈕、購物車數量    |

## API
### 登入相關 API 
#### 
```
Method: GET
Path: /cosign/token_login_page
Parameters: token
Usage: use for login verify token
```

 情境       | 參數         | 預期結果        |
 ----------- | ------------- | ----------- |
 正常 token | 合法 JWT        | Request 被接受 |
 缺少 token | 無             | Request 被拒  |
 空 token  | `token=`      | Request 被拒  |
 非 JWT 格式 | `abc123`      | Request 被拒  |
 非字串      | `token=12345` | Request 被拒  |

```
Method: POST
Path: /api/platform-sdk/otp-verification
Parameters: 
  - Header: x-platform-token
  - Body: account, otpCode, purpose
Usage: verify OTP code for login (SMS-based authentication)
Body json:
{
  "account": "+886936727490",
  "otpCode": "234222",
  "purpose": "login"
}

```

| 情境          | 參數合                                                           | 預期結果        |
| ----------- | -------------------------------------------------------------- | ----------- |
| 正常請求        | 合法 `x-platform-token` + 正確 `account / otpCode / purpose=login` | Request 被接受 |
| 缺少平台 token  | 無 `x-platform-token`                                           | Request 被拒  |
| OTP 格式錯誤    | `otpCode=123`（長度不足）                                            | Request 被拒  |
| 帳號與 OTP 不匹配 | 正確格式 OTP + 錯誤 `account`                                        | Request 被拒  |
| 不支援用途       | `purpose=register`                                             | Request 被拒  |

```
Method: POST
Path: /api/platform-sdk/otp
Parameters:
  - Header: x-platform-token
  - Body: account, countryCode, otpTemplateSettingKey, recaptchaToken,
          type, redirectUrl, fallbackUrl, purpose, validateUrl
Usage: request OTP (SMS) for login or authentication
Body json: 
{
  "account": "+886936727490",
  "countryCode": "TW",
  "otpTemplateSettingKey": "TW_zh_TW",
  "recaptchaToken": "<recaptcha_token>",
  "type": "sms",
  "purpose": "login",
  "redirectUrl": "https://www.dogcatstar.com/product/respiratory-health/?no-cache=",
  "fallbackUrl": "https://www.dogcatstar.com/product/respiratory-health/?no-cache=",
  "validateUrl": "https://www.dogcatstar.com/my-account/?validate=registerOrLogin"
}

```
| 情境           | 參數                                                                    | 預期結果        |
| ------------ | --------------------------------------------------------------------- | ----------- |
| 正常請求         | 合法 `x-platform-token` + 正確 `account / recaptchaToken / purpose=login` | Request 被接受 |
| 缺少平台 token   | 無 `x-platform-token`                                                  | Request 被拒  |
| 缺少帳號         | 無 `account`                                                           | Request 被拒  |
| reCAPTCHA 無效 | `recaptchaToken` 為過期或錯誤值                                              | Request 被拒  |
| 不支援用途        | `purpose=register`（非預期值）                                              | Request 被拒  |


### 購物車相關 API
####
```
Method: POST
Path: /api/ec/v2/TW/cart/calculate
Parameters (Body JSON):
- billing_country
- project_code
- country_code
- order_items
- manual_input_coupon_ids
- applied_shipping_method_id
- language
- cart_values
Usage: calculate cart price, shipping, promotion, and payment summary
```
| 情境                               | 參數                                  | 預期結果             |
| -------------------------------- | ----------------------------------- | ---------------- |
| 正常請求                             | 所有必填欄位皆存在且格式正確                      | Request 被接受（200） |
| 缺少 `order_items`                 | `order_items` 不存在                   | Request 被拒（400）  |
| `order_items` 為空陣列               | `order_items: []`                   | Request 被拒（400）  |
| `quantity` 為 0 或 負數                  | `order_items[0].quantity = 0`       | Request 被拒（400）  |
| `applied_shipping_method_id` 非數字 | `"applied_shipping_method_id": "2"` | Request 被拒（400）  |


```
Method: POST
Path: /api/events
Parameters (Body JSON):
- event
Usage: collect frontend behavior events for analytics / tracking
Body json:
{
  "event": {
    "app_env": "production",
    "event_name": "add_to_cart",
    "project_code": "DCS",
    "country_code": "TW",
    "event_id": "uuid",
    "ga_client_id": "string",
    "event_info": {
      "status_code": "001",
      "status_message": "ATC Success",
      "currency": "TWD",
      "value": null,
      "items": [ ... ],
      "session_id": "string",
      "document_title": "string",
      "document_location": "url"
    }
  }
}
```
| 情境                | 參數                      | 預期結果                   |
| ----------------- | ----------------------- | ---------------------- |
| 正常事件送出            | event 結構完整且格式正確         | Request 被接受（200 / 204） |
| 缺少 `event`        | body 無 `event` key      | Request 被拒（400）        |
| 缺少 `event_name`   | `event.event_name` 不存在  | Request 被拒（400）        |
| `event_id` 非 UUID | `event_id = "12345"`    | Request 被拒（400）        |
| `items` 非陣列       | `event_info.items = {}` | Request 被拒（400）        |


## TODO:
- [ ] (product_page_helper.py) 有時候按太快會沒反應，暫時用 wait_for_load_state 解決，感覺是在等 API 回應？
- [ ] (mailotp.py) 根據實際 OTP 格式調整正則表達式，目前只是假設 OTP 是 6 位數字
- [ ] (login_page.py) 目前自動登入後判斷已經登入的等待策略不好，應該改進
- [ ] 目前網頁跳轉都是直接用網址，完整 E2E 應該也要有按鈕連結跳轉



## Bug
https://www.dogcatstar.com/product/chickenfishessence/ 可以只選綜合 40g * 20 包一盒，不選口味就加入購物車，但是選擇的是單包 40g 4 包
