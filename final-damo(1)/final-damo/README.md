# 🛡️ Web 應用安全防禦實驗室 (WAF Demo)



## 🚀 實驗三階段實作指引

### 🔹 階段一：無防護狀態 (DetectionOnly)
**情境：** WAF 僅作為監視器，不進行攔截；後端程式碼無任何過濾邏輯。
* **準備工作：** - `compose.yaml` 設定 `MODSEC_RULE_ENGINE=DetectionOnly`
    - `app.py` 設定偵測到 `OR` 時回傳 `Success`
* **執行攻擊：**
    ```bash
    docker exec -it client1 curl -v "[http://172.20.0.254:8080/?user='OR'1'='1](http://172.20.0.254:8080/?user='OR'1'='1)"
    ```
* **觀察重點：**
    - **回應結果：** `HTTP 200 OK` 且看到 `Login Success (SQLi bypass)`。
    - **Server Log：** `docker logs server` 會出現狀態碼 **200**，證明攻擊穿透。
    - **WAF Log：** 顯示 `Warning` 但動作為 `Pass`。

---

### 🔹 階段二：應用層過濾 (Application Filter)
**情境：** WAF 仍不攔截，但工程師手動修改程式碼，由後端 Python 進行安全檢查。
* **準備工作：** - 修改 `app.py`：偵測到攻擊特徵時 `return "...", 403`
    - 重啟服務：`docker compose up -d server`
* **執行攻擊：**
    ```bash
    docker exec -it client1 curl -v "[http://172.20.0.254:8080/?user='OR'1'='1](http://172.20.0.254:8080/?user='OR'1'='1)"
    ```
* **觀察重點：**
    - **回應結果：** `HTTP 403 Forbidden` 且內容為自訂的 `<h1>` 標籤。
    - **Server Log：** `docker logs server` 會出現狀態碼 **403**，代表流量已抵達後端才被攔截。
    - **缺點：** 後端伺服器仍需消耗運算資源處理惡意請求。

---

### 🔹 階段三：WAF 強制防護 (WAF Blocking)
**情境：** 開啟 WAF 的自動攔截功能，在惡意封包抵達伺服器前就直接阻斷。
* **準備工作：** - `compose.yaml` 修改為 `MODSEC_RULE_ENGINE=On`
    - 重啟 WAF：`docker compose up -d waf`
* **執行攻擊：**
    ```bash
    docker exec -it client1 curl -v "[http://172.20.0.254:8080/?user='OR'1'='1](http://172.20.0.254:8080/?user='OR'1'='1)"
    ```
* **觀察重點：**
    - **回應結果：** `HTTP 403 Forbidden` 且內容為 **Nginx 預設頁面**。
    - **Server Log：** `docker logs server` **完全沒有任何新紀錄**。
    - **WAF Log：** 顯示關鍵紀錄 `Access denied with code 403`。

---

## 📊 實驗對比總結

| 觀察項目 | 階段一：無防護 | 階段二：應用層過濾 | 階段三：WAF 防護 |
| :--- | :--- | :--- | :--- |
| **WAF 模式** | DetectionOnly | DetectionOnly | **On (Enabled)** |
| **回應狀態碼** | 200 OK | 403 Forbidden | 403 Forbidden |
| **阻斷者** | 無 | Python 程式碼 | **WAF (Nginx)** |
| **後端日誌紀錄** | 有 (200) | 有 (403) | **無 (完全阻斷)** |
| **資源消耗** | 高 | 中 | **極低** |

---

## 🔍 快速檢查指令

* **查看 WAF 攔截判決 (Windows CMD):**
  ```cmd
  docker logs waf | findstr "Access denied"

* **重看 Server 流量紀錄:**
  ```cmd
  docker logs server
