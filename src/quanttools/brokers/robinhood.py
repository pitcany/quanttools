import os
from quanttools.execution import ExecutionHandler


class RobinhoodExecutionHandler(ExecutionHandler):
    """
    ExecutionHandler that uses the unofficial robin_stocks wrapper
    to send live orders to Robinhood.
    """

    def __init__(self, username: str = None, password: str = None):
        """
        Initialize RobinhoodExecutionHandler by logging into Robinhood.

        :param username: Robinhood username or env var ROBINHOOD_USER
        :param password: Robinhood password or env var ROBINHOOD_PASS
        """
        import robin_stocks as r

        username = username or os.getenv("ROBINHOOD_USER")
        password = password or os.getenv("ROBINHOOD_PASS")
        if not username or not password:
            raise RuntimeError("ROBINHOOD_USER/ROBINHOOD_PASS must be set")
        self._robin = r
        self._robin.login(username, password)

    def send_order(self, symbol: str, quantity: int, order_type: str = "market") -> None:
        """
        Send a market order for a symbol; positive quantity for buy, negative for sell.
        """
        r = self._robin
        if order_type != "market":
            raise NotImplementedError("RobinhoodExecutionHandler only supports market orders.")
        if quantity > 0:
            r.orders.order_buy_market(symbol, quantity)
        else:
            r.orders.order_sell_market(symbol, abs(quantity))
