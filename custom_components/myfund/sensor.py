"""Sensor platform for MyFund integration."""
import logging
from datetime import timedelta
from json import JSONDecodeError

import aiohttp
import async_timeout
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up MyFund sensor based on a config entry."""
    coordinator = MyFundDataUpdateCoordinator(hass, config_entry)
    await coordinator.async_config_entry_first_refresh()

    entities = [
        MyFundTotalValueSensor(coordinator, config_entry),
    ]

    async_add_entities(entities)


class MyFundDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize."""
        self.api_key = config_entry.data["api_key"]
        self.wallet_name = config_entry.data["wallet_name"]
        update_minutes = config_entry.options.get("update_interval") or config_entry.data.get("update_interval", 5)

        super().__init__(
            hass,
            _LOGGER,
            name="MyFund",
            update_interval=timedelta(minutes=update_minutes),
        )

    async def _async_update_data(self):
        """Update data via library."""
        url = f"https://myfund.pl/API/v1/getPortfel.php?portfel={self.wallet_name}&apiKey={self.api_key}&format=json"

        try:
            async with aiohttp.ClientSession() as session:
                with async_timeout.timeout(10):
                    async with session.get(url) as response:
                        response_text = await response.text()

                        # Parse JSON manually since server returns wrong content-type
                        import json
                        data = json.loads(response_text)

                        if str(data.get("status", {}).get("code")) == "1":
                            raise UpdateFailed(f"Error: {data.get('status', {}).get('text')}")

                        return data
        except JSONDecodeError as err:
            raise UpdateFailed(f"Invalid JSON response: {err}")
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")


class MyFundTotalValueSensor(SensorEntity):
    """Representation of MyFund total portfolio value sensor."""

    def __init__(self, coordinator: MyFundDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._attr_name = f"MyFund {config_entry.data['wallet_name']} Total Value"
        self._attr_unique_id = f"myfund_{config_entry.entry_id}_total_value"
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._attr_native_unit_of_measurement = "PLN"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.coordinator.data:
            return self.coordinator.data.get("portfel", {}).get("wartosc")
        return None

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success
