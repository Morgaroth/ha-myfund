import logging
from datetime import timedelta
from json import JSONDecodeError

import aiohttp
import async_timeout
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)

class MyFundDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize."""
        self.api_key = config_entry.data["api_key"]
        self.wallet_name = config_entry.data["wallet_name"]
        update_minutes = config_entry.options.get("update_interval") or config_entry.data.get("update_interval", 5)
        
        _LOGGER.debug("Initializing coordinator for wallet: %s with %d minute interval", self.wallet_name, update_minutes)

        super().__init__(
            hass,
            _LOGGER,
            name="MyFund",
            update_interval=timedelta(minutes=update_minutes),
        )
        
        _LOGGER.debug("Coordinator initialized, update interval: %s", self.update_interval)

    async def _async_update_data(self):
        """Update data via library."""
        url = f"https://myfund.pl/API/v1/getPortfel.php?portfel={self.wallet_name}&apiKey={self.api_key}&format=json"
        
        _LOGGER.debug("Starting data update for wallet: %s", self.wallet_name)

        try:
            async with aiohttp.ClientSession() as session:
                with async_timeout.timeout(10):
                    _LOGGER.debug("Making API request to: %s", url)
                    async with session.get(url) as response:
                        response_text = await response.text()
                        _LOGGER.debug("Received response: %s", response_text[:200])

                        # Parse JSON manually since server returns wrong content-type
                        import json
                        data = json.loads(response_text)

                        if str(data.get("status", {}).get("code")) == "1":
                            _LOGGER.error("API returned error: %s", data.get('status', {}).get('text'))
                            raise UpdateFailed(f"Error: {data.get('status', {}).get('text')}")

                        _LOGGER.debug("Successfully parsed data for wallet: %s", self.wallet_name)
                        return data
        except JSONDecodeError as err:
            _LOGGER.error("Failed to parse JSON response: %s", err)
            raise UpdateFailed(f"Invalid JSON response: {err}")
        except Exception as err:
            _LOGGER.error("Error communicating with API: %s", err)
            raise UpdateFailed(f"Error communicating with API: {err}")
