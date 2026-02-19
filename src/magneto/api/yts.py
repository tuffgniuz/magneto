import httpx


class YTSClient:
    """Async client for the YTS API."""

    DOMAINS = [
        "https://yts.bz",
        "https://yts.mx",
        "https://yts.lt",
        "https://yts.am",
    ]

    HEADERS = {
        "User-Agent": "Mozilla/5.0",
    }

    def __init__(self):
        self.base_url: str | None = None

    async def _find_working_domain(self, client: httpx.AsyncClient) -> str:
        """Try each domain until one responds."""
        for domain in self.DOMAINS:
            try:
                url = f"{domain}/api/v2/list_movies.json?limit=1"
                response = await client.get(url, timeout=10)
                if response.status_code == 200:
                    return domain
            except (httpx.RequestError, httpx.TimeoutException):
                continue
        raise ConnectionError("No working YTS domain found.")

    async def list_movies(self, page: int = 1, limit: int = 20, query_term: str | None = None) -> list[dict]:
        """Fetch a list of movies. Returns a list of movie dicts."""
        async with httpx.AsyncClient(
            follow_redirects=True,
            headers=self.HEADERS,
            timeout=15.0,
        ) as client:
            if not self.base_url:
                self.base_url = await self._find_working_domain(client)

            url = f"{self.base_url}/api/v2/list_movies.json"

            params = {"page": page, "limit": limit}

            if query_term:
                params["query_term"] = query_term

            response = await client.get(url, params=params)
            response.raise_for_status()

            data = response.json()
            return data["data"].get("movies", [])

    async def get_movie_details(self, movie_id: int) -> dict:
        """Fetch details for a specific movie."""
        async with httpx.AsyncClient(
            follow_redirects=True,
            headers=self.HEADERS,
            timeout=15.0,
        ) as client:
            if not self.base_url:
                self.base_url = await self._find_working_domain(client)

            url = f"{self.base_url}/api/v2/movie_details.json"
            params = {"movie_id": movie_id}
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data["data"].get("movie", {})
