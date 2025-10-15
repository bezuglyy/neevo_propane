
from __future__ import annotations
from typing import Any
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import DOMAIN, CONF_TOKEN, CONF_DEVICE_ID, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
from .api import NeevoClient, NeevoApiError

class NeevoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        errors: dict[str, str] = {}
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=vol.Schema({
                vol.Required(CONF_TOKEN): str,
            }))
        token = user_input[CONF_TOKEN].strip()
        session = async_get_clientsession(self.hass)
        client = NeevoClient(session, token)
        try:
            devices = await client.fetch_devices()
        except NeevoApiError as e:
            errors["base"] = "invalid_auth" if "invalid_auth" in str(e) else "cannot_connect"
            return self.async_show_form(step_id="user", data_schema=vol.Schema({
                vol.Required(CONF_TOKEN, default=token): str,
            }), errors=errors)

        if not devices:
            errors["base"] = "cannot_connect"
            return self.async_show_form(step_id="user", data_schema=vol.Schema({
                vol.Required(CONF_TOKEN, default=token): str,
            }), errors=errors)

        self._devices = devices
        self._token = token

        choices = {}
        for dev in devices:
            dev_id = str(dev.get("DeviceId") or dev.get("Name"))
            label = f"{dev.get('Name','Device')} ({dev.get('DeviceId')})"
            choices[dev_id] = label

        return self.async_show_form(
            step_id="pick_device",
            data_schema=vol.Schema({ vol.Required(CONF_DEVICE_ID): vol.In(choices) })
        )

    async def async_step_pick_device(self, user_input: dict[str, Any]) -> FlowResult:
        device_id = user_input[CONF_DEVICE_ID]
        await self.async_set_unique_id(device_id)
        self._abort_if_unique_id_configured()
        data = { CONF_TOKEN: self._token, CONF_DEVICE_ID: device_id }
        return self.async_create_entry(title=f"Neevo {device_id}", data=data)

    async def async_get_options_flow(self, entry: config_entries.ConfigEntry):
        return NeevoOptionsFlow(entry)

class NeevoOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, entry: config_entries.ConfigEntry) -> None:
        self.entry = entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(CONF_SCAN_INTERVAL, default=self.entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)): int
            })
        )
