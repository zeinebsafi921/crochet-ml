"""
Ravelry API Client

This module handles all communication with the Ravelry API.
It provides a clean interface for fetching crochet pattern data.
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class RavelryClient:
    """
    A client for interacting with the Ravelry API.
    
    Attributes:
        base_url: The base URL for all API requests
        auth: A tuple of (username, password) for authentication
    """

    BASE_URL = "https://api.ravelry.com"

    def __init__(self):
        """
        Initialize the client by loading credentials from environment variables.
        Raises ValueError if credentials are missing.
        """
        username = os.getenv("RAVELRY_USERNAME")
        password = os.getenv("RAVELRY_PASSWORD")

        if not username or not password:
            raise ValueError(
                "Ravelry credentials not found. "
                "Make sure RAVELRY_USERNAME and RAVELRY_PASSWORD "
                "are set in your .env file."
            )

        self.auth = (username, password)

    def search_patterns(
        self,
        query: str = "",
        craft: str = "crochet",
        page: int = 1,
        page_size: int = 100,
    ) -> dict:
        """
        Search for patterns on Ravelry.

        Args:
            query: Search term (e.g. 'granny square', 'amigurumi')
            craft: Type of craft - 'crochet' or 'knitting'
            page: Page number for pagination
            page_size: Number of results per page (max 100)

        Returns:
            A dictionary containing pattern results and pagination info
        """
        endpoint = f"{self.BASE_URL}/patterns/search.json"

        params = {
            "query": query,
            "craft": craft,
            "page": page,
            "page_size": page_size,
            "sort": "popularity",
        }

        response = requests.get(endpoint, auth=self.auth, params=params)
        response.raise_for_status()

        return response.json()

    def get_pattern(self, pattern_id: int) -> dict:
        """
        Fetch detailed information about a single pattern.

        Args:
            pattern_id: The unique Ravelry ID of the pattern

        Returns:
            A dictionary containing full pattern details
        """
        endpoint = f"{self.BASE_URL}/patterns/{pattern_id}.json"

        response = requests.get(endpoint, auth=self.auth)
        response.raise_for_status()

        return response.json()["pattern"]