"""
Module for data loading and retrieval.
"""

class DataLoader:
    """
    Abstract interface for fetching historical market data.
    Subclass this to implement specific data sources.
    """
    def get_data(self, symbol: str, start: str, end: str):
        """
        Fetch historical price data for a given symbol and date range.

        :param symbol: Asset symbol (e.g., 'AAPL').
        :param start: Start date (YYYY-MM-DD).
        :param end: End date (YYYY-MM-DD).
        :returns: Sequence of records with price and volume information.
        """
        raise NotImplementedError("DataLoader.get_data must be implemented by subclass.")
