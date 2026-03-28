# AI Binance Trade

你也想成為交易達人嗎？

但是複雜的技術分析、混淆視聽的新聞面，總是搞得你頭昏眼花？

**現在你可以訓練一個屬於你自己的 AI Agent。**

讓它學會你的交易策略，24小時幫你盯盤、判斷進場、執行交易。

不再需要盯著螢幕，不再需要猜測市場。

---

## 它能做什麼？

### 📈 交易
現貨、期貨、槓桿——全部交給 AI 掌控。
```python
ai.spot_buy("BTCUSDT", 0.001, price=67000)
ai.futures_buy("BTC", 0.001, stop_loss=60000, take_profit=70000)
```

### 💰 理財
閒置資金自動放進 Staking / Savings，靠利息幫你賺錢。
```python
ai.staking_purchase("STAKING", "BNB", 10)
ai.defi_stake("ETH", 0.5)
```

### 🔄 借貸
質押加密借 USDT，資金不閒置。
```python
ai.loan_borrow("USDT", 100, collateral_coin="BTC", collateral_amount=0.01)
```

### 🔀 轉帳
帳戶間調配資金，一個指令就完成。
```python
ai.transfer("USDT", 50, "spot", "futures")
ai.convert("BTC", "USDT", 0.01)
```

### 🔍 查詢
餘額、倉位、價格——即時掌握。
```python
ai.balance()
ai.positions()
ai.price("BTCUSDT")
```

---

## 為什麼用它？

| 你自己盯盤 | AI Agent 幫你 |
|-----------|--------------|
| ❌ 睡覺就错过機會 | ✅ 24/7 自動交易 |
| ❌ 情緒影響判斷 | ✅ 完全服從紀律 |
| ❌ 反應太慢 | ✅ 毫秒級執行 |
| ❌ 手動操作太累 | ✅ 躺著就能賺 |

---

## 支援的功能

| 類別 | 功能 |
|------|------|
| **現貨交易** | spot_buy, spot_sell, spot_cancel |
| **期貨交易** | futures_buy, futures_sell, futures_close |
| **理財** | staking_purchase, staking_redeem, defi_stake |
| **借貸** | loan_borrow, loan_repay, isolated_loan_borrow |
| **轉帳** | transfer, futures_transfer, deposit, withdraw |
| **兌換** | convert, convert_quote |
| **查詢** | balance, positions, price, wallet |

---

## 快速開始

```bash
pip install -r requirements.txt
export BINANCE_API_KEY="你的Key"
export BINANCE_API_SECRET="你的Secret"
```

```python
from ai_binance_trade import AIBinance

ai = AIBinance()

# AI 幫你判斷 → 執行交易
ai.spot_buy("BTCUSDT", 0.001, price=67000)
```

---

## 版本

**v1.0.0** - 完整版，支援所有主要功能

---

## 警告

⚠️ 加密貨幣交易有風險。AI 決策可能導致損失。請謹慎操作。

---

## 支援這個專案

如果你想支持開發者，這是推薦連結：

👉 https://www.binance.com/referral/earn-together/refer2earn-usdc/claim?hl=zh-TC&ref=GRO_28502_H0O1M&utm_source=default
