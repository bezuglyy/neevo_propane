
from __future__ import annotations
from typing import Any, List
import aiohttp
from .const import API_URL

class NeevoApiError(Exception):
    pass

class NeevoClient:
    def __init__(self, session: aiohttp.ClientSession, token: str) -> None:
        self._session = session
        self._token = token  # base64 string WITHOUT 'Basic '

    async def fetch_devices(self) -> list[dict[str, Any]]:
        headers = {
            "Authorization": f"Basic {self._token}",
            "Content-Type": "application/json",
        }
        async with self._session.get(API_URL, headers=headers, timeout=aiohttp.ClientTimeout(total=20)) as resp:
            if resp.status == 401:
                raise NeevoApiError("invalid_auth")
            if resp.status >= 400:
                raise NeevoApiError(f"http_{resp.status}")
            data = await resp.json(content_type=None)
            if not isinstance(data, list):
                raise NeevoApiError("unexpected_payload")
            return data
