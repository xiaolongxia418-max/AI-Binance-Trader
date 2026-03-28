# AI Binance Trade - Ultimate Edition

**Train your own AI Agent for fully automated crypto trading.**

---

Want to become a trading pro, but confused by complex technical analysis and overwhelming market noise?

Now you can train your own AI Agent, let it learn your trading strategy, and have it monitor markets 24/7, identify entries, and execute trades automatically.

**No more staring at screens. No more guessing.**

---

## 🎁 Get Started with Binance

👉 **[Sign up via this link and get rewards](https://www.binance.com/referral/earn-together/refer2earn-usdc/claim?hl=zh-TC&ref=GRO_28502_H0O1M&utm_source=default)**

---

## Features

### 📈 Trading Automation
```python
# Spot buy
ai.spot_buy("BTCUSDT", 0.001, price=67000)

# Futures long
ai.futures_buy("BTC", 0.001,
               stop_loss=60000,
               take_profit=70000)

# Futures short
ai.futures_sell("ETH", 1,
                 stop_loss=2200,
                 take_profit=1800)

# Close position
ai.futures_close("BTC")
ai.close_all_positions()  # Close all
```

### 💰 Automated Earn
```python
# Staking
ai.staking_purchase("STAKING", "BNB", 10)

# DeFi stake (ETH 2.0)
ai.defi_stake("ETH", 0.5)

# Redeem
ai.staking_redeem("STAKING", "BNB", amount=5)
```

### 🔄 Loan
```python
# Borrow USDT using BTC as collateral
ai.loan_borrow("USDT", 100,
                collateral_coin="BTC",
                collateral_amount=0.01)

# Repay
ai.loan_repay("USDT", 50)
```

### 🔀 Transfer
```python
# Spot → Futures
ai.transfer("USDT", 100, "spot", "futures")

# Convert
ai.convert("BTC", "USDT", 0.01)

# Deposit address
ai.deposit_address("USDT")

# Withdraw
ai.withdraw("USDT", 50, address="wallet_address")
```

### 🔍 Query
```python
ai.balance()              # USDT balance
ai.total_balance()         # Total balance
ai.price("BTCUSDT")       # Real-time price
ai.positions()            # All positions
ai.open_orders()          # Pending orders
ai.order_book("BTCUSDT")  # Order book
ai.wallet()               # Full wallet
```

---

## Complete Function Reference

### Spot Trading
| Function | Description |
|----------|-------------|
| `spot_buy(symbol, amount, price)` | Spot buy |
| `spot_sell(symbol, amount, price)` | Spot sell |
| `spot_cancel(order_id, symbol)` | Cancel order |

### Futures Trading
| Function | Description |
|----------|-------------|
| `futures_buy(symbol, amount, sl, tp)` | Open long |
| `futures_sell(symbol, amount, sl, tp)` | Open short |
| `futures_close(symbol)` | Close position |
| `futures_set_leverage(symbol, lev)` | Set leverage |

### Staking / Earn
| Function | Description |
|----------|-------------|
| `staking_purchase(product, product_id, amount)` | Purchase staking |
| `staking_redeem(product, product_id, amount)` | Redeem staking |
| `staking_balance()` | Staking balance |
| `defi_stake(product, amount)` | DeFi stake |
| `defi_unstake(product, amount)` | DeFi unstake |

### Loan
| Function | Description |
|----------|-------------|
| `loan_borrow(coin, amount, col_coin, col_amt)` | Borrow crypto |
| `loan_repay(coin, amount)` | Repay loan |
| `loan_balance()` | Loan positions |
| `isolated_loan_borrow(symbol, coin, amount)` | Isolated margin borrow |

### Transfer
| Function | Description |
|----------|-------------|
| `transfer(coin, amt, from, to)` | Internal transfer |
| `futures_transfer(coin, amt, from, to)` | Spot-Futures transfer |
| `deposit_address(coin, network)` | Get deposit address |
| `withdraw(coin, amt, addr, network, tag)` | Withdraw |
| `deposit_history(coin)` | Deposit history |
| `withdraw_history(coin)` | Withdraw history |

### Convert
| Function | Description |
|----------|-------------|
| `convert(from_coin, to_coin, amount)` | Convert coin |
| `convert_quote(from_coin, to_coin, amount)` | Get convert quote |

### Query
| Function | Description |
|----------|-------------|
| `balance(coin)` | Balance query |
| `total_balance(coin)` | Total balance |
| `all_balances()` | All coin balances |
| `price(symbol)` | Price query |
| `prices(symbols)` | Multiple prices |
| `positions(symbol)` | Position query |
| `open_orders(symbol)` | Open orders |
| `trade_history(symbol, limit)` | Trade history |
| `wallet()` | Full wallet |

### Strategy Tools
| Function | Description |
|----------|-------------|
| `dca(symbol, amount, n, dir)` | Dollar cost averaging |
| `grid_orders(symbol, lo, hi, n, amt)` | Grid orders |
| `cancel_all_orders(symbol)` | Cancel all orders |
| `close_all_positions()` | Close all positions |

---

## AI Agent Usage Examples

### Example 1: Trend Following
```python
ai = AIBinance()

# AI analyzes and decides to enter
if ai_analysis_says_bullish():
    ai.futures_buy("BTC", 0.001,
                   stop_loss=calculate_support(),
                   take_profit=calculate_resistance())
```

### Example 2: DCA Strategy
```python
# AI decides to accumulate gradually
ai.dca("BTCUSDT",
        amount=100,      # Total 100 USDT
        intervals=4,     # Split into 4 buys
        direction="buy")
```

### Example 3: Auto Earn
```python
# Put idle BNB into staking
bnb_bal = ai.balance("BNB")
if bnb_bal > 1:
    ai.staking_purchase("STAKING", "BNB", bnb_bal * 0.8)
```

### Example 4: Loan Liquidity
```python
# Borrow USDT using BTC as collateral
ai.loan_borrow("USDT", 100,
                collateral_coin="BTC",
                collateral_amount=0.01)
```

---

## Installation

```bash
pip install -r requirements.txt
```

Set environment variables:
```bash
export BINANCE_API_KEY="your_api_key"
export BINANCE_API_SECRET="your_api_secret"
```

Or in code:
```python
ai = AIBinance(
    api_key="your_api_key",
    api_secret="your_api_secret"
)
```

---

## API Permissions

| Function | Required Permission |
|----------|-------------------|
| Trading, Query | Spot / Futures trading |
| Staking | Savings services |
| Transfer | Account transfer |
| Withdraw | Withdrawal |

Recommended: Enable "Spot + Futures + Savings" permissions when creating your Binance API key.

---

## FAQ

**Q: Is this Skill safe?**
A: Your API key is only used for trading within your own Binance account. All operations stay in your account.

**Q: How do I train the AI Agent?**
A: This Skill provides execution functions. The AI's training depends on your AI Agent platform (e.g., OpenClaw).

**Q: How much capital do I need?**
A: Recommended minimum is $100 USDT to start trading.

---

## Warning

⚠️ Cryptocurrency trading involves risk. AI decisions may result in significant losses. Trade responsibly.
