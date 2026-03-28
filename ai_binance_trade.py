#!/usr/bin/env python3
"""
AI Binance Trade - Ultimate Edition
Complete Binance API wrapper for AI Agents.
Covers: Spot, Futures, Staking, Savings, Loan, Transfer, and more.
"""
from __future__ import annotations

import os
import time
from typing import Optional, List, Dict, Any

import ccxt


# ============================================================
# Exceptions
# ============================================================

class BinanceAPIError(Exception):
    """Binance API error."""
    pass


# ============================================================
# Main Class
# ============================================================

class AIBinance:
    """
    Complete Binance API wrapper for AI Agents.
    
    Organized into modules:
    - trading: Spot, Futures, Options
    - staking: Staking, Savings, Dual
    - loan: Crypto-backed loans
    - transfer: Internal, Convert, Deposit, Withdraw
    - info: Balance, Positions, Prices
    """
    
    def __init__(
        self,
        api_key: str = None,
        api_secret: str = None,
        testnet: bool = False
    ):
        self.api_key = api_key or os.getenv("BINANCE_API_KEY", "")
        self.api_secret = api_secret or os.getenv("BINANCE_API_SECRET", "")
        self.testnet = testnet
        
        if not self.api_key or not self.api_secret:
            raise ValueError(
                "API keys required. Set BINANCE_API_KEY and BINANCE_API_SECRET "
                "as environment variables, or pass them to constructor."
            )
        
        self.exchange = self._create_exchange()
        self.exchange.load_markets()
    
    def _create_exchange(self) -> ccxt.Exchange:
        config = {
            "enableRateLimit": True,
            "apiKey": self.api_key,
            "secret": self.api_secret,
            "options": {"defaultType": "spot"},
        }
        
        if self.testnet:
            config["urls"] = {
                "api": "https://testnet.binance.vision"
            }
        
        return ccxt.binance(config)
    
    def _retry_call(self, fn, *args, **kwargs):
        delay = 1.0
        for i in range(5):
            try:
                return fn(*args, **kwargs)
            except Exception as e:
                if "RateLimit" in str(e) or "429" in str(e):
                    time.sleep(delay)
                    delay = min(delay * 2, 30)
                    continue
                raise
        raise RuntimeError("Max retries exceeded")
    
    def _round_amount(self, symbol: str, amount: float) -> float:
        try:
            return float(self.exchange.amount_to_precision(symbol, amount))
        except Exception:
            return float(amount)
    
    def _round_price(self, symbol: str, price: float) -> float:
        try:
            return float(self.exchange.price_to_precision(symbol, price))
        except Exception:
            return float(price)
    
    # ============================================================
    # INFO - Account & Market Information
    # ============================================================
    
    def balance(self, coin: str = "USDT") -> float:
        """Get balance for a coin. Default USDT."""
        bal = self._retry_call(self.exchange.fetch_balance)
        coin = coin.upper()
        if coin in bal:
            b = bal[coin]
            if isinstance(b, dict):
                return float(b.get("free") or 0)
            return float(b)
        return float(bal.get("free", {}).get(coin, 0))
    
    def total_balance(self, coin: str = "USDT") -> float:
        """Get total balance (free + used) for a coin."""
        bal = self._retry_call(self.exchange.fetch_balance)
        coin = coin.upper()
        if coin in bal:
            b = bal[coin]
            if isinstance(b, dict):
                return float(b.get("total") or 0)
            return float(b)
        return 0.0
    
    def all_balances(self) -> Dict[str, Dict[str, float]]:
        """Get all balances."""
        bal = self._retry_call(self.exchange.fetch_balance)
        result = {}
        for coin, data in bal.items():
            if isinstance(data, dict):
                free = float(data.get("free") or 0)
                total = float(data.get("total") or 0)
                if total > 0:
                    result[coin] = {"free": free, "total": total}
        return result
    
    def price(self, symbol: str) -> float:
        """Get current price for symbol."""
        ticker = self._retry_call(
            self.exchange.fetch_ticker,
            symbol.upper().strip()
        )
        return float(ticker.get("last") or ticker.get("close") or 0)
    
    def prices(self, symbols: List[str] = None) -> Dict[str, float]:
        """Get prices for multiple symbols."""
        if symbols:
            prices = {}
            for sym in symbols:
                try:
                    prices[sym.upper()] = self.price(sym)
                except Exception:
                    pass
            return prices
        return {}
    
    def order_book(self, symbol: str, limit: int = 20) -> Dict[str, Any]:
        """Get order book."""
        ob = self._retry_call(
            self.exchange.fetch_order_book,
            symbol.upper().strip(), limit
        )
        return {
            "bids": ob.get("bids", [])[:limit],
            "asks": ob.get("asks", [])[:limit],
            "timestamp": ob.get("timestamp")
        }
    
    def positions(self, symbol: str = None) -> List[Dict[str, Any]]:
        """Get open positions."""
        try:
            raw = self._retry_call(self.exchange.fetch_positions)
        except Exception:
            raw = []
        
        positions = []
        for pos in raw:
            contracts = pos.get("contracts") or pos.get("size") or 0
            if float(contracts) == 0:
                continue
            if symbol and pos.get("symbol", "").upper() != symbol.upper():
                continue
            
            positions.append({
                "symbol": pos.get("symbol"),
                "side": pos.get("side", "").upper(),
                "amount": float(contracts),
                "entry_price": float(pos.get("entryPrice") or pos.get("average") or 0),
                "leverage": float(pos.get("leverage") or 1),
                "unrealized_pnl": float(pos.get("unrealizedPnl") or 0),
                "timestamp": pos.get("timestamp")
            })
        
        return positions
    
    def open_orders(self, symbol: str = None) -> List[Dict[str, Any]]:
        """Get open orders."""
        if symbol:
            return self._retry_call(
                self.exchange.fetch_open_orders,
                symbol.upper()
            )
        return self._retry_call(self.exchange.fetch_open_orders)
    
    def trade_history(self, symbol: str = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Get trade history."""
        if symbol:
            return self._retry_call(
                self.exchange.fetch_my_trades,
                symbol.upper(), None, limit
            )
        return []
    
    def wallet(self) -> Dict[str, Any]:
        """Get full wallet information."""
        return self._retry_call(self.exchange.fetch_balance)
    
    # ============================================================
    # SPOT TRADING
    # ============================================================
    
    def spot_buy(
        self,
        symbol: str,
        amount: float,
        price: float = None
    ) -> Dict[str, Any]:
        """
        Buy on spot market.
        
        Args:
            symbol: Trading pair (e.g., "BTCUSDT")
            amount: Quantity to buy
            price: Limit price (None for market order)
        """
        symbol = symbol.upper().strip().replace("/", "")
        amount = self._round_amount(symbol, amount)
        
        if price:
            order = self._retry_call(
                self.exchange.create_order,
                symbol, "limit", "buy", amount, self._round_price(symbol, price)
            )
        else:
            order = self._retry_call(
                self.exchange.create_order,
                symbol, "market", "buy", amount
            )
        
        return {
            "success": True,
            "order_id": order.get("id"),
            "symbol": symbol,
            "side": "BUY",
            "amount": amount,
            "price": order.get("average") or order.get("price"),
            "timestamp": order.get("timestamp")
        }
    
    def spot_sell(
        self,
        symbol: str,
        amount: float,
        price: float = None
    ) -> Dict[str, Any]:
        """
        Sell on spot market.
        
        Args:
            symbol: Trading pair (e.g., "BTCUSDT")
            amount: Quantity to sell
            price: Limit price (None for market order)
        """
        symbol = symbol.upper().strip().replace("/", "")
        amount = self._round_amount(symbol, amount)
        
        if price:
            order = self._retry_call(
                self.exchange.create_order,
                symbol, "limit", "sell", amount, self._round_price(symbol, price)
            )
        else:
            order = self._retry_call(
                self.exchange.create_order,
                symbol, "market", "sell", amount
            )
        
        return {
            "success": True,
            "order_id": order.get("id"),
            "symbol": symbol,
            "side": "SELL",
            "amount": amount,
            "price": order.get("average") or order.get("price"),
            "timestamp": order.get("timestamp")
        }
    
    def spot_cancel(self, order_id: str, symbol: str) -> Dict[str, Any]:
        """Cancel a spot order."""
        try:
            self._retry_call(
                self.exchange.cancel_order,
                order_id, symbol.upper().replace("/", "")
            )
            return {"success": True, "order_id": order_id}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ============================================================
    # FUTURES TRADING
    # ============================================================
    
    def futures_buy(
        self,
        symbol: str,
        amount: float,
        price: float = None,
        stop_loss: float = None,
        take_profit: float = None
    ) -> Dict[str, Any]:
        """
        Open a LONG futures position.
        
        Args:
            symbol: Futures pair (e.g., "BTCUSDT")
            amount: Contract quantity
            price: Entry price (None for market)
            stop_loss: Stop loss price
            take_profit: Take profit price
        """
        symbol = symbol.upper().strip().replace("/", "") + "/USDT:USDT"
        amount = self._round_amount(symbol, amount)
        
        params = {}
        
        if stop_loss:
            params["stopPrice"] = self._round_price(symbol, stop_loss)
            params["triggerPrice"] = self._round_price(symbol, stop_loss)
        
        if take_profit:
            params["takeProfitPrice"] = self._round_price(symbol, take_profit)
        
        # Set one-way mode
        params["side"] = "BUY"
        params["positionSide"] = "LONG"
        
        if price:
            order = self._retry_call(
                self.exchange.create_order,
                symbol, "limit", "buy", amount, self._round_price(symbol, price), params
            )
        else:
            order = self._retry_call(
                self.exchange.create_order,
                symbol, "market", "buy", amount, None, params
            )
        
        return {
            "success": True,
            "order_id": order.get("id"),
            "symbol": symbol,
            "side": "BUY",
            "amount": amount,
            "price": order.get("average") or order.get("price"),
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "timestamp": order.get("timestamp")
        }
    
    def futures_sell(
        self,
        symbol: str,
        amount: float,
        price: float = None,
        stop_loss: float = None,
        take_profit: float = None
    ) -> Dict[str, Any]:
        """
        Open a SHORT futures position.
        """
        symbol = symbol.upper().strip().replace("/", "") + "/USDT:USDT"
        amount = self._round_amount(symbol, amount)
        
        params = {}
        
        if stop_loss:
            params["stopPrice"] = self._round_price(symbol, stop_loss)
            params["triggerPrice"] = self._round_price(symbol, stop_loss)
        
        if take_profit:
            params["takeProfitPrice"] = self._round_price(symbol, take_profit)
        
        params["side"] = "SELL"
        params["positionSide"] = "SHORT"
        
        if price:
            order = self._retry_call(
                self.exchange.create_order,
                symbol, "limit", "sell", amount, self._round_price(symbol, price), params
            )
        else:
            order = self._retry_call(
                self.exchange.create_order,
                symbol, "market", "sell", amount, None, params
            )
        
        return {
            "success": True,
            "order_id": order.get("id"),
            "symbol": symbol,
            "side": "SELL",
            "amount": amount,
            "price": order.get("average") or order.get("price"),
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "timestamp": order.get("timestamp")
        }
    
    def futures_close(self, symbol: str) -> Dict[str, Any]:
        """Close a futures position."""
        positions = self.positions(symbol)
        if not positions:
            return {"success": False, "message": "No open position"}
        
        position = positions[0]
        side = "sell" if position["side"] == "LONG" else "buy"
        symbol_full = symbol.upper().replace("/", "") + "/USDT:USDT"
        
        order = self._retry_call(
            self.exchange.create_order,
            symbol_full, "market", side, position["amount"],
            None, {"reduceOnly": True}
        )
        
        return {
            "success": True,
            "order_id": order.get("id"),
            "closed_side": position["side"],
            "amount": position["amount"],
            "timestamp": order.get("timestamp")
        }
    
    def futures_set_leverage(self, symbol: str, leverage: int) -> Dict[str, Any]:
        """Set leverage for a futures symbol."""
        symbol = symbol.upper().replace("/", "") + "/USDT:USDT"
        leverage = max(1, min(leverage, 125))
        
        try:
            self._retry_call(
                self.exchange.set_leverage,
                leverage, symbol
            )
            return {"success": True, "leverage": leverage}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ============================================================
    # STAKING / EARN
    # ============================================================
    
    def staking_purchase(
        self,
        product: str,
        product_id: str,
        amount: float,
        renewable: bool = False
    ) -> Dict[str, Any]:
        """
        Purchase staking product.
        
        Args:
            product: Product type ( "STAKING", "LOCKED_SAVINGS", "FLEXIBLE")
            product_id: Product ID
            amount: Amount to stake
            renewable: Enable auto-renew
        """
        try:
            # Try flexible savings
            result = self.exchange.sapi_post_savings_purchase({
                "productId": product_id,
                "amount": str(amount),
                "type": "NEXT"
            })
            return {"success": True, "result": result}
        except Exception as e:
            # Try locked staking
            try:
                result = self.exchange.sapi_post_staking_purchase({
                    "productId": product_id,
                    "amount": str(amount),
                    "renewable": str(renewable).lower()
                })
                return {"success": True, "result": result}
            except Exception as e2:
                return {"success": False, "error": str(e2)}
    
    def staking_redeem(
        self,
        product: str,
        product_id: str,
        amount: float = None,
        all: bool = False
    ) -> Dict[str, Any]:
        """
        Redeem from staking.
        
        Args:
            product: Product type
            product_id: Product ID
            amount: Amount to redeem (None if all=True)
            all: Redeem all
        """
        try:
            params = {"productId": product_id}
            if all:
                params["type"] = "REDEMPTION"
            else:
                params["type"] = "NORMAL"
                params["amount"] = str(amount)
            
            result = self.exchange.sapi_post_savings_redeem(params)
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def staking_balance(self) -> Dict[str, Any]:
        """Get staking balance."""
        try:
            result = self.exchange.sapi_get_savings_account()
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def defi_stake(
        self,
        product: str,
        amount: float
    ) -> Dict[str, Any]:
        """
        Stake in DeFi products (ETH 2.0, etc.)
        """
        try:
            result = self.exchange.sapi_post_eth_stake({
                "amount": str(amount)
            })
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def defi_unstake(
        self,
        product: str = "ETH",
        amount: float = None,
        all: bool = False
    ) -> Dict[str, Any]:
        """Unstake from DeFi."""
        try:
            params = {}
            if all:
                params["type"] = "FULL"
            else:
                params["type"] = "PARTIAL"
                params["amount"] = str(amount)
            
            result = self.exchange.sapi_post_eth_unstake(params)
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ============================================================
    # LOAN / MARGIN
    # ============================================================
    
    def loan_borrow(
        self,
        coin: str,
        amount: float,
        collateral_coin: str = "BNB",
        collateral_amount: float = None
    ) -> Dict[str, Any]:
        """
        Borrow crypto via margin/loan.
        """
        try:
            params = {
                "asset": coin.upper(),
                "amount": str(amount)
            }
            if collateral_coin and collateral_amount:
                params["collateralAsset"] = collateral_coin.upper()
                params["collateralAmount"] = str(collateral_amount)
            
            result = self.exchange.sapi_post_margin_borrow(params)
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def loan_repay(
        self,
        coin: str,
        amount: float
    ) -> Dict[str, Any]:
        """Repay margin loan."""
        try:
            result = self.exchange.sapi_post_margin_repay({
                "asset": coin.upper(),
                "amount": str(amount)
            })
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def loan_balance(self) -> Dict[str, Any]:
        """Get cross margin borrow info."""
        try:
            result = self.exchange.sapi_get_margin_account()
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def isolated_loan_borrow(
        self,
        symbol: str,
        coin: str,
        amount: float
    ) -> Dict[str, Any]:
        """Borrow on isolated margin for a specific pair."""
        try:
            result = self.exchange.sapi_post_margin_isolated_borrow({
                "asset": coin.upper(),
                "symbol": symbol.upper().replace("/", ""),
                "amount": str(amount)
            })
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ============================================================
    # TRANSFER
    # ============================================================
    
    def transfer(
        self,
        coin: str,
        amount: float,
        from_account: str,
        to_account: str
    ) -> Dict[str, Any]:
        """
        Transfer between Binance accounts.
        
        Account types: SPOT, FUTURES, OPTION, MINING, FINANCIAL, FUTURES_DELIVERY, MARGIN
        """
        account_types = {
            "spot": "SPOT",
            "futures": "UMFUTURE",  # USD-M Futures
            "delivery": "CMFUTURE",  # COIN-M Futures
            "margin": "MARGE",
            "mining": "MINING"
        }
        
        from_type = account_types.get(from_account.lower(), from_account.upper())
        to_type = account_types.get(to_account.lower(), to_account.upper())
        
        try:
            result = self.exchange.sapi_post_account_transfer({
                "asset": coin.upper(),
                "amount": str(amount),
                "type": 1,  # Universal transfer
                "fromAccountType": from_type,
                "toAccountType": to_type
            })
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def futures_transfer(
        self,
        coin: str,
        amount: float,
        from_account: str = "spot",
        to_account: str = "futures"
    ) -> Dict[str, Any]:
        """Transfer between spot and futures."""
        side = 1 if from_account == "spot" else 2
        
        try:
            result = self.exchange.sapi_post_futures_transfer({
                "asset": coin.upper(),
                "amount": str(amount),
                "type": side
            })
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def deposit_address(self, coin: str, network: str = None) -> Dict[str, Any]:
        """Get deposit address."""
        try:
            params = {"coin": coin.upper()}
            if network:
                params["network"] = network.upper()
            
            result = self.exchange.sapi_get_capital_deposit_address(params)
            return {
                "success": True,
                "address": result.get("address"),
                "tag": result.get("tag"),
                "network": result.get("network"),
                "coin": coin.upper()
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def withdraw(
        self,
        coin: str,
        amount: float,
        address: str,
        network: str = None,
        tag: str = None
    ) -> Dict[str, Any]:
        """Withdraw to external wallet."""
        try:
            params = {
                "coin": coin.upper(),
                "amount": str(amount),
                "address": address
            }
            if network:
                params["network"] = network.upper()
            if tag:
                params["addressTag"] = tag
            
            result = self.exchange.sapi_post_capital_withdraw_apply(params)
            return {
                "success": True,
                "withdraw_id": result.get("id"),
                "coin": coin.upper(),
                "amount": amount,
                "address": address,
                "timestamp": result.get("withdrawOrderId")
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def deposit_history(self, coin: str = None, limit: int = 100) -> Dict[str, Any]:
        """Get deposit history."""
        try:
            params = {"limit": limit}
            if coin:
                params["coin"] = coin.upper()
            
            result = self.exchange.sapi_get_capital_deposit_history(params)
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def withdraw_history(self, coin: str = None, limit: int = 100) -> Dict[str, Any]:
        """Get withdraw history."""
        try:
            params = {"limit": limit}
            if coin:
                params["coin"] = coin.upper()
            
            result = self.exchange.sapi_get_capital_withdraw_history(params)
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ============================================================
    # CONVERT
    # ============================================================
    
    def convert(
        self,
        from_coin: str,
        to_coin: str,
        amount: float
    ) -> Dict[str, Any]:
        """Convert one coin to another."""
        try:
            result = self.exchange.sapi_post_convert_transfer({
                "fromAsset": from_coin.upper(),
                "toAsset": to_coin.upper(),
                "amount": str(amount)
            })
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def convert_quote(
        self,
        from_coin: str,
        to_coin: str,
        amount: float
    ) -> Dict[str, Any]:
        """Get convert quote before executing."""
        try:
            result = self.exchange.sapi_get_convert_get_quote({
                "fromAsset": from_coin.upper(),
                "toAsset": to_coin.upper(),
                "amount": str(amount)
            })
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ============================================================
    # STRATEGY HELPERS
    # ============================================================
    
    def dca(
        self,
        symbol: str,
        amount: float,
        intervals: int = 4,
        direction: str = "buy"
    ) -> List[Dict[str, Any]]:
        """
        Dollar Cost Averaging - spread buy/sell over multiple orders.
        """
        results = []
        per_order = amount / intervals
        
        for i in range(intervals):
            try:
                if direction.lower() == "buy":
                    result = self.spot_buy(symbol, per_order)
                else:
                    result = self.spot_sell(symbol, per_order)
                results.append(result)
                time.sleep(0.5)
            except Exception as e:
                results.append({"success": False, "error": str(e)})
        
        return results
    
    def grid_orders(
        self,
        symbol: str,
        lower_price: float,
        upper_price: float,
        grid_count: int = 5,
        amount_per_grid: float = 0.001
    ) -> List[Dict[str, Any]]:
        """
        Create a basic grid of orders.
        """
        results = []
        price_step = (upper_price - lower_price) / grid_count
        
        for i in range(grid_count):
            buy_price = lower_price + (price_step * i)
            sell_price = lower_price + (price_step * (i + 1))
            
            try:
                # Place buy order at this level
                buy_order = self.spot_buy(symbol, amount_per_grid, buy_price)
                results.append({"grid_level": i, "buy": buy_order})
                
                # Place sell order above
                sell_order = self.spot_sell(symbol, amount_per_grid, sell_price)
                results.append({"grid_level": i, "sell": sell_order})
                
            except Exception as e:
                results.append({"success": False, "error": str(e)})
        
        return results
    
    # ============================================================
    # UTILITY
    # ============================================================
    
    def set_leverage(self, symbol: str, leverage: int) -> Dict[str, Any]:
        """Set leverage (alias for futures)."""
        return self.futures_set_leverage(symbol, leverage)
    
    def cancel_order(self, order_id: str, symbol: str) -> Dict[str, Any]:
        """Cancel order (alias for spot)."""
        return self.spot_cancel(order_id, symbol)
    
    def cancel_all_orders(self, symbol: str = None) -> Dict[str, Any]:
        """Cancel all open orders."""
        try:
            if symbol:
                self._retry_call(
                    self.exchange.cancel_all_orders,
                    symbol.upper().replace("/", "")
                )
            else:
                orders = self.open_orders()
                for o in orders:
                    try:
                        self.spot_cancel(o["id"], o["symbol"])
                    except Exception:
                        pass
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def close_all_positions(self) -> List[Dict[str, Any]]:
        """Close all open positions."""
        results = []
        for pos in self.positions():
            try:
                result = self.futures_close(pos["symbol"])
                results.append(result)
            except Exception as e:
                results.append({"success": False, "error": str(e)})
        return results


# ============================================================
# Aliases
# ============================================================

class BinanceTrader(AIBinance):
    """Alias for AIBinance - backward compatibility."""
    pass


# ============================================================
# CLI Interface
# ============================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Binance Trade - Ultimate Edition")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Balance
    p_balance = subparsers.add_parser("balance", help="Check balance")
    p_balance.add_argument("--coin", default="USDT", help="Coin to check")
    
    # Prices
    p_price = subparsers.add_parser("price", help="Get price")
    p_price.add_argument("symbol", help="Trading pair")
    
    # Buy/Sell
    p_buy = subparsers.add_parser("buy", help="Buy spot")
    p_buy.add_argument("symbol", help="Trading pair")
    p_buy.add_argument("amount", type=float, help="Amount")
    p_buy.add_argument("--price", type=float, help="Limit price")
    
    p_sell = subparsers.add_parser("sell", help="Sell spot")
    p_sell.add_argument("symbol", help="Trading pair")
    p_sell.add_argument("amount", type=float, help="Amount")
    p_sell.add_argument("--price", type=float, help="Limit price")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    binance = AIBinance()
    
    if args.command == "balance":
        bal = binance.balance(args.coin)
        print(f"Balance: {bal} {args.coin}")
    
    elif args.command == "price":
        price = binance.price(args.symbol)
        print(f"{args.symbol}: {price}")
    
    elif args.command == "buy":
        result = binance.spot_buy(args.symbol, args.amount, args.price)
        print(result)
    
    elif args.command == "sell":
        result = binance.spot_sell(args.symbol, args.amount, args.price)
        print(result)


if __name__ == "__main__":
    main()
