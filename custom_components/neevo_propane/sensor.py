
from __future__ import annotations
from typing import Any
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from .coordinator import NeevoCoordinator

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:
    coordinator: NeevoCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([NeevoLevelSensor(coordinator), NeevoTempSensor(coordinator)], update_before_add=True)

class BaseNeevoSensor(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator: NeevoCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_device_info = {
            "identifiers": {(DOMAIN, str(coordinator.device_id))},
            "name": f"Neevo Propane {coordinator.device_id}",
            "manufacturer": "OtoData (Neevo)",
            "model": "Wireless Tank Monitor",
        }

    @property
    def available(self) -> bool:
        return bool(self.coordinator.data)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        d = self.coordinator.data or {}
        attrs = {}
        for k in ("DeviceId", "Name", "SerialNumber", "Pressure", "LastUpdated"):
            v = d.get(k)
            if v is not None:
                attrs[k] = v
        return attrs

class NeevoLevelSensor(BaseNeevoSensor):
    _attr_name = "Level"
    _attr_native_unit_of_measurement = "%"

    @property
    def unique_id(self) -> str:
        return f"{self.coordinator.device_id}_level"

    @property
    def native_value(self):
        d = self.coordinator.data or {}
        try:
            return float(d.get("Level"))
        except (TypeError, ValueError):
            return None

class NeevoTempSensor(BaseNeevoSensor):
    _attr_name = "Temperature"
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = "°C"

    @property
    def unique_id(self) -> str:
        return f"{self.coordinator.device_id}_temperature"

    @property
    def native_value(self):
        d = self.coordinator.data or {}
        t = d.get("Temperature")
        try:
            return float(t) if t is not None else None
        except (TypeError, ValueError):
            return None
