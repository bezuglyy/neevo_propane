
from __future__ import annotations
from datetime import timedelta
from typing import Any
import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DEFAULT_SCAN_INTERVAL
from .api import NeevoClient, NeevoApiError

_LOGGER = logging.getLogger(__name__)

class NeevoCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    def __init__(self, hass: HomeAssistant, client: NeevoClient, device_id: str, scan_interval: int | None) -> None:
        self.client = client
        self.device_id = device_id
        interval = timedelta(seconds=scan_interval or DEFAULT_SCAN_INTERVAL)
        super().__init__(
            hass,
            logger=_LOGGER,
            name=f"Neevo Propane ({device_id})",
            update_interval=interval,
        )

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            devices = await self.client.fetch_devices()
        except NeevoApiError as err:
            raise UpdateFailed(str(err)) from err
        if not devices:
            return {}
        # match by DeviceId or Name (string compare)
        for item in devices:
            if str(item.get("DeviceId")) == str(self.device_id) or str(item.get("Name")) == str(self.device_id):
                return item
        # fallback to first device
        return devices[0]
