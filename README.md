# AI Binance Trade - Ultimate Edition

**訓練你自己的 AI Agent，實現全自動交易。**

---

你也想成為交易達人，但是複雜的技術分析、混淆視聽的新聞面總是搞得你頭昏眼花嗎？

現在你可以訓練一個屬於你自己的 AI Agent，讓它學會你的交易策略，24小時幫你盯盤、判斷進場、執行交易。

不再需要盯著螢幕，不再需要猜測市場。

---

## 功能一覽

### 📈 交易自動化
```python
# 現貨買入
ai.spot_buy("BTCUSDT", 0.001, price=67000)

# 期貨開多
ai.futures_buy("BTC", 0.001,
               stop_loss=60000,
               take_profit=70000)

# 期貨開空
ai.futures_sell("ETH", 1,
                 stop_loss=2200,
                 take_profit=1800)

# 平倉
ai.futures_close("BTC")
ai.close_all_positions()  # 全部平倉
```

### 💰 自動理財
```python
# Staking 質押
ai.staking_purchase("STAKING", "BNB", 10)

# DeFi 質押 (ETH 2.0)
ai.defi_stake("ETH", 0.5)

# 贖回
ai.staking_redeem("STAKING", "BNB", amount=5)
```

### 🔄 借貸
```python
# 質押借貸
ai.loan_borrow("USDT", 100,
                collateral_coin="BTC",
                collateral_amount=0.01)

# 還款
ai.loan_repay("USDT", 50)
```

### 🔀 帳戶轉帳
```python
# 現貨 → 期貨
ai.transfer("USDT", 100, "spot", "futures")

# 幣種兌換
ai.convert("BTC", "USDT", 0.01)

# 入金地址
ai.deposit_address("USDT")

# 出金
ai.withdraw("USDT", 50, address="錢包地址")
```

### 🔍 查詢功能
```python
ai.balance()              # USDT 餘額
ai.total_balance()         # 總餘額（含倉位）
ai.price("BTCUSDT")       # 即時價格
ai.positions()            # 所有倉位
ai.open_orders()          # 掛單
ai.order_book("BTCUSDT")  # 訂單簿
ai.wallet()               # 完整錢包
```

---

## 完整函數列表

### 現貨交易
| 函數 | 說明 |
|------|------|
| `spot_buy(symbol, amount, price)` | 現貨買入 |
| `spot_sell(symbol, amount, price)` | 現貨賣出 |
| `spot_cancel(order_id, symbol)` | 取消現貨訂單 |

### 期貨交易
| 函數 | 說明 |
|------|------|
| `futures_buy(symbol, amount, sl, tp)` | 開多單 |
| `futures_sell(symbol, amount, sl, tp)` | 開空單 |
| `futures_close(symbol)` | 平倉 |
| `futures_set_leverage(symbol, lev)` | 設定槓桿 |
| `set_leverage(symbol, lev)` | 設定槓桿（別名）|

### 理財 / Staking
| 函數 | 說明 |
|------|------|
| `staking_purchase(product, product_id, amount)` | 申購理財 |
| `staking_redeem(product, product_id, amount)` | 贖回理財 |
| `staking_balance()` | 理財餘額 |
| `defi_stake(product, amount)` | DeFi 質押 |
| `defi_unstake(product, amount)` | DeFi 解除質押 |

### 借貸
| 函數 | 說明 |
|------|------|
| `loan_borrow(coin, amount, col_coin, col_amt)` | 質押借貸 |
| `loan_repay(coin, amount)` | 還款 |
| `loan_balance()` | 借貸倉位 |
| `isolated_loan_borrow(symbol, coin, amount)` | 逐倉借貸 |

### 轉帳
| 函數 | 說明 |
|------|------|
| `transfer(coin, amt, from, to)` | 帳戶間轉帳 |
| `futures_transfer(coin, amt, from, to)` | 現貨期貨轉帳 |
| `deposit_address(coin, network)` | 取得入金地址 |
| `withdraw(coin, amt, addr, network, tag)` | 出金 |
| `deposit_history(coin)` | 入金紀錄 |
| `withdraw_history(coin)` | 出金紀錄 |

### 兌換
| 函數 | 說明 |
|------|------|
| `convert(from_coin, to_coin, amount)` | 幣種兌換 |
| `convert_quote(from_coin, to_coin, amount)` | 取得兌換報價 |

### 查詢
| 函數 | 說明 |
|------|------|
| `balance(coin)` | 餘額查詢 |
| `total_balance(coin)` | 總餘額 |
| `all_balances()` | 所有幣種餘額 |
| `price(symbol)` | 價格查詢 |
| `prices(symbols)` | 多幣種價格 |
| `positions(symbol)` | 倉位查詢 |
| `open_orders(symbol)` | 掛單查詢 |
| `trade_history(symbol, limit)` | 交易紀錄 |
| `wallet()` | 完整錢包 |

### 策略工具
| 函數 | 說明 |
|------|------|
| `dca(symbol, amount, n, dir)` | 分批買入/賣出 |
| `grid_orders(symbol, lo, hi, n, amt)` | 網格訂單 |
| `cancel_all_orders(symbol)` | 取消全部掛單 |
| `close_all_positions()` | 全部平倉 |

---

## AI Agent 使用範例

### 範例 1：趨勢追蹤
```python
ai = AIBinance()

# AI 分析完覺得可以進場
if ai_analysis_says_bullish():
    ai.futures_buy("BTC", 0.001,
                   stop_loss=calculate_support(),
                   take_profit=calculate_resistance())
```

### 範例 2：定投策略
```python
# AI 決定分批買入
ai.dca("BTCUSDT",
       amount=100,      # 總共 100 USDT
       intervals=4,     # 分 4 次
       direction="buy")
```

### 範例 3：自動理財
```python
# 把閒置的 BNB 質押
bnb_bal = ai.balance("BNB")
if bnb_bal > 1:
    ai.staking_purchase("STAKING", "BNB", bnb_bal * 0.8)
```

### 範例 4：借貸流動性
```python
# 質押 BTC 借 USDT
ai.loan_borrow("USDT", 100,
                collateral_coin="BTC",
                collateral_amount=0.01)
```

---

## 安裝方式

```bash
pip install -r requirements.txt
```

設定環境變數：
```bash
export BINANCE_API_KEY="你的API_KEY"
export BINANCE_API_SECRET="你的API_SECRET"
```

或在程式碼中：
```python
ai = AIBinance(
    api_key="你的API_KEY",
    api_secret="你的API_SECRET"
)
```

---

## API 權限需求

| 功能 | 需要的權限 |
|------|-----------|
| 交易、查詢 | 現貨 / 期貨交易 |
| 理財質押 | 理財服務 |
| 轉帳 | 帳戶轉帳 |
| 出金 | 提現 |

建議在 Binance 建立 API 時開啟「現貨 + 期貨 + 理財」權限。

---

## 常見問題

**Q: 這個 Skill 安全嗎？**
A: 你的 API Key 只用來執行交易，所有操作都在你自己的 Binance 帳戶中。

**Q: AI Agent 怎麼訓練？**
A: 這個 Skill 提供執行功能，AI 的訓練取決於你使用的 AI Agent 平台（如 OpenClaw）。

**Q: 需要多少資金？**
A: 建議至少 $100 USDT 開始交易。

---

## 警告

⚠️ 加密貨幣交易有風險。AI 決策可能導致損失。請謹慎操作。

---

## Binance 推薦連結

👉 [使用此連結註冊 Binance 並獲得獎勵](https://www.binance.com/referral/earn-together/refer2earn-usdc/claim?hl=zh-TC&ref=GRO_28502_H0O1M&utm_source=default)
