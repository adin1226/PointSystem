# 點數兌換網站DEMO

雲端連結: https://pointsystem-k60w.onrender.com

## 專案介紹

本專案為一個點數兌換系統，提供會員透過點數兌換商品和店家刊登商品功能。

系統有以下功能：

* 會員與店家註冊 / 登入
* 會員
  * 儲值點數
  * 兌換商品
  * 查看交易紀錄
* 店家
  * 刊登商品
  * 更改商品數量/價格
  * 下架商品

---

## 技術使用

* Backend: Python + Django
* API Framework: Django REST Framework
* Authentication: Token Authentication
* Database: SQLite
* Frontend: Bootstrap 5 + HTML + JS
* 套件使用: 請見 requirement.txt

---

### Token 取得方式
有些需要登入的 API，需在 request header 中帶入 Access Token
1. 用curl打 /api/login 取得
2. 在網頁裡登入後，進入DevTools -> Application -> Local storage 複製access這個key的value即可

---

## API 說明

#### Login

POST /api/login/

```json
{
  "username": "ben",
  "password": "123456"
}
```

Response:

```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "role": "member"
}
```

---

#### Register

POST /api/register/

```json
{
  "username": "ben",
  "password": "123456",
  "role": "member"
}
```

Response:

```json
{
  "username": "ben",
  "role": "member"
}
```

---

#### Deposit（需登入）: 會員儲值點數

POST /api/users/deposit/

Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

```json
{
  "amount": 100,
}
```

測試範例 (in Windows cmd):
```cmd
curl -X POST http://127.0.0.1:8000/api/users/deposit/ ^
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ..." ^
  -H "Content-Type: application/json" ^
  -d "{\"amount\":100}"
```

Response:

```json
{
  "message": "Points added",
  "points":700
}
```

---

#### Exchange（需登入）: 會員兌換商品

POST /api/exchange/

Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

```json
{
  "product_id": 1
}
```

測試範例 (in Windows cmd):
```cmd
curl -X POST http://127.0.0.1:8000/api/exchange/ ^
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." ^
  -H "Content-Type: application/json" ^
  -d "{\"product_id\":1}"
```

Response:

```json
{
  "message":"Exchange successful",
  "remaining_points":700,
  "transaction":
  {
    "id":14,
    "product_name":"test",
    "points_used":2000,
    "created_at":"2026-05-10T04:33:32.207781+08:00"
  }
}
```

---

#### 取得會員兌換紀錄

GET /api/member_transactions

Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

---

#### 刊登商品 (需登入且只有店家能刊登)

POST /api/products/create/

Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

```json
{
  "name": "iPhone",
  "points_required": 3000,
  "stock": 1
}
```
---

#### 下架商品

DELETE /api/products/<product_id>/delete/

Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

```json
{
  "message": "Product deleted"
}
```

---

#### 更新商品(價格跟庫存)

PUT /api/products/<product_id>/update/

Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

```json
{
  "stock": 1,
  "points_required": 100
}
```

---

## 如何啟動

### 安裝套件

```bash
pip install -r requirements.txt
```

---

### Migration

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 啟動伺服器

```bash
python manage.py runserver 0.0.0.0:8000
```

---

### 開啟系統

* 前台首頁
  http://127.0.0.1:8000/

---

## 資料庫設計

### User

| 欄位       | 說明     |
| -------- | ------ |
| id       | 使用者 ID |
| username | 帳號     |
| password | 密碼（加密） |
| points   | 點數     |
| role   | 身分(店家or會員)     |

---

### Product

| 欄位              | 說明    |
| --------------- | ----- |
| id              | 商品 ID |
| name            | 商品名稱  |
| points_required | 所需點數  |
| stock           | 庫存    |
| owner_id     | 刊登商家ID  |

---

### Transaction

| 欄位          | 說明    |
| ----------- | ----- |
| id          | 交易 ID |
| points_used | 使用點數  |
| created_at  | 交易建立時間  |
| product_id     | 商品ID    |
| user_id        | 使用者ID   |

---
