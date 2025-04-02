"""The iDisplay integration."""
import logging
import requests
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers import entity_registry as er
from datetime import timedelta

from .const import DOMAIN, CONF_USER_LOGIN, CONF_SERVER_URL, CONF_INTERVAL

# Define that this integration is set up via config entries only
CONFIG_SCHEMA = cv.config_entry_only_config_schema("idisplay")

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the iDisplay component."""
    return True

def is_number(value):
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False

async def send_sensor_data(hass, entry):
    """Collect sensor data and send it to the external server."""
    config = entry.data
    if not config.get(CONF_USER_LOGIN):
        _LOGGER.warning("iDisplay login is not provided. Skipping data send.")
        return

    entity_registry = er.async_get(hass)
    payload = {}

    for entity_id in entity_registry.entities:
        bins = entity_id.startswith("binary_sensor.");
        if entity_id.startswith("sensor.") or bins:
            sid = entity_id.replace("sensor.", "")
            state = hass.states.get(entity_id)
            if state:
                value = state.state
                unit = state.attributes.get("unit_of_measurement", "")
                if bins:
                    value = 0 if value == "off" else 1;
                elif not is_number(value):
                        unit = value # store textual value in the unit field
                        value = None # empty value field completely
                payload[sid] = {
                    "v": value,
                    "u": unit,
                    "n": state.attributes.get("friendly_name", sid)  # Use id as a fallback
                }

    try:
        url = f"{CONF_SERVER_URL}?login={config[CONF_USER_LOGIN]}"
        response = await hass.async_add_executor_job(
            lambda: requests.post(url, json=payload)
        )
        response.raise_for_status()
        _LOGGER.info(f"Data sent successfully: {payload}")
    except Exception as e:
        _LOGGER.error(f"Failed to send data: {e}")

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up iDisplay from a config entry."""
    # Schedule the function to run periodically using the constant interval
    interval = timedelta(seconds=CONF_INTERVAL)

    # Use a lambda to properly await the async function
    async def _wrapper(_):
        await send_sensor_data(hass, entry)

    async_track_time_interval(hass, _wrapper, interval)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return True
