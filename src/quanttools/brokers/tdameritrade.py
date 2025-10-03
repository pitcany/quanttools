import os
from quanttools.execution import ExecutionHandler


class TDAExecutionHandler(ExecutionHandler):
    """
    ExecutionHandler for TD Ameritrade API. Supports market and limit orders.
    """

    def __init__(
        self,
        api_key: str = None,
        redirect_uri: str = None,
        token_path: str = "tda_token.json",
    ):
        """
        Initialize TDAExecutionHandler and load/refresh OAuth token.

        :param api_key: TD Ameritrade API key or env var TDA_API_KEY
        :param redirect_uri: OAuth redirect URI or env var TDA_REDIRECT_URI
        :param token_path: File path for storing OAuth token
        """
        from tda import auth

        api_key = api_key or os.getenv("TDA_API_KEY")
        redirect_uri = redirect_uri or os.getenv("TDA_REDIRECT_URI")
        if not api_key or not redirect_uri:
            raise RuntimeError("TDA_API_KEY/TDA_REDIRECT_URI must be set")
        self._client = auth.client_from_token_file(token_path, api_key, redirect_uri)

    def send_order(self, symbol: str, quantity: int, order_type: str = "market") -> None:
        from tda.orders import equities, OrderBuilder

        account_id = os.getenv("TDA_ACCOUNT_ID")
        if not account_id:
            raise RuntimeError("TDA_ACCOUNT_ID must be set")

        if order_type == "market":
            if quantity > 0:
                order_spec = equities.equity_buy_market(symbol, quantity)
            else:
                order_spec = equities.equity_sell_market(symbol, abs(quantity))
        else:
            # Example limit order; user should override or extend as needed.
            limit_price = None
            order_spec = (
                OrderBuilder.equity(symbol, quantity > 0)
                .limit_limit_price(limit_price)
                .build()
            )

        response = self._client.place_order(account_id=account_id, order_spec=order_spec)
        response.raise_for_status()
