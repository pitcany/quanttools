"""
Module for handling order execution interfaces.
"""


class ExecutionHandler:
    """
    Abstract interface for sending orders to a broker or simulator.
    """
    def send_order(self, symbol: str, quantity: int, order_type: str = "market") -> None:
        """
        Send an order to the market or broker API.

        :param symbol: Asset symbol (e.g., 'AAPL').
        :param quantity: Number of units to buy (>0) or sell (<0).
        :param order_type: Order type, e.g., 'market', 'limit'.
        """
        raise NotImplementedError("ExecutionHandler.send_order must be implemented by subclass.")
