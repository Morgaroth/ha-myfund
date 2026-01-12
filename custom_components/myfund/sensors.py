import logging

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import DeviceInfo

from custom_components.myfund.update_coordinator import MyFundDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


class MyFundPortfolioSensor(SensorEntity):
    """General MyFund portfolio sensor with all data as attributes."""
    
    _attr_has_entity_name = True

    def __init__(self, coordinator: MyFundDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._attr_translation_key = "portfolio"
        self._attr_unique_id = f"myfund_{config_entry.entry_id}"
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._attr_device_info = DeviceInfo(
            identifiers={("myfund", config_entry.entry_id)},
            name=f"MyFund {config_entry.data['wallet_name']}",
            manufacturer="MyFund.pl",
        )

    @property
    def native_value(self):
        """Return the total value as the main sensor value."""
        if self.coordinator.data:
            return self.coordinator.data.get("portfel", {}).get("wartosc")
        return None

    @property
    def native_unit_of_measurement(self):
        """Return the unit of measurement."""
        if self.coordinator.data:
            return self.coordinator.data.get("portfel", {}).get("waluta")
        return None

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
        if not self.coordinator.data:
            return {}

        portfel = self.coordinator.data.get("portfel", {})

        def parse_change(value):
            if isinstance(value, str):
                return float(value.replace("+", ""))
            return value

        return {
            "daily_change": portfel.get("zmianaDzienna"),
            "profit": portfel.get("zysk"),
            "weekly_change": parse_change(portfel.get("zmianaW")),
            "2weekly_change": parse_change(portfel.get("zmiana2W")),
            "monthly_change": parse_change(portfel.get("zmianaM")),
            "3monthly_change": parse_change(portfel.get("zmiana3M")),
            "6monthly_change": parse_change(portfel.get("zmiana6M")),
            "yearly_change": parse_change(portfel.get("zmianaR")),
            "currency": portfel.get("waluta"),
        }

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success


class MyFundTotalValueSensor(SensorEntity):
    """Representation of MyFund total portfolio value sensor."""
    
    _attr_has_entity_name = True

    def __init__(self, coordinator: MyFundDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._attr_translation_key = "total_value"
        self._attr_unique_id = f"myfund_{config_entry.entry_id}_total_value"
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._attr_device_info = DeviceInfo(
            identifiers={("myfund", config_entry.entry_id)},
            name=f"MyFund {config_entry.data['wallet_name']}",
            manufacturer="MyFund.pl",
        )

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.coordinator.data:
            return self.coordinator.data.get("portfel", {}).get("wartosc")
        return None

    @property
    def native_unit_of_measurement(self):
        """Return the unit of measurement."""
        if self.coordinator.data:
            return self.coordinator.data.get("portfel", {}).get("waluta")
        return None

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success


class MyFundDailyChangeSensor(SensorEntity):
    """Daily change sensor."""
    
    _attr_has_entity_name = True

    def __init__(self, coordinator: MyFundDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        self.coordinator = coordinator
        self._attr_translation_key = "daily_change"
        self._attr_unique_id = f"myfund_{config_entry.entry_id}_daily_change"
        self._attr_native_unit_of_measurement = "%"
        self._attr_device_info = DeviceInfo(
            identifiers={("myfund", config_entry.entry_id)},
            name=f"MyFund {config_entry.data['wallet_name']}",
            manufacturer="MyFund.pl",
        )

    @property
    def native_value(self):
        if self.coordinator.data:
            return self.coordinator.data.get("portfel", {}).get("zmianaDzienna")
        return None

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success


class MyFundProfitSensor(SensorEntity):
    """Profit sensor."""
    
    _attr_has_entity_name = True

    def __init__(self, coordinator: MyFundDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        self.coordinator = coordinator
        self._attr_translation_key = "profit"
        self._attr_unique_id = f"myfund_{config_entry.entry_id}_profit"
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._attr_device_info = DeviceInfo(
            identifiers={("myfund", config_entry.entry_id)},
            name=f"MyFund {config_entry.data['wallet_name']}",
            manufacturer="MyFund.pl",
        )

    @property
    def native_value(self):
        if self.coordinator.data:
            return self.coordinator.data.get("portfel", {}).get("zysk")
        return None

    @property
    def native_unit_of_measurement(self):
        """Return the unit of measurement."""
        if self.coordinator.data:
            return self.coordinator.data.get("portfel", {}).get("waluta")
        return None

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success


class MyFundChangeSensor(SensorEntity):
    """Generic change sensor."""
    
    _attr_has_entity_name = True

    def __init__(self, coordinator: MyFundDataUpdateCoordinator, config_entry: ConfigEntry, field_key: str,
                 translation_key: str, unique_suffix: str) -> None:
        self.coordinator = coordinator
        self.field_key = field_key
        self._attr_translation_key = translation_key
        self._attr_unique_id = f"myfund_{config_entry.entry_id}_{unique_suffix}_change"
        self._attr_native_unit_of_measurement = "%"
        self._attr_device_info = DeviceInfo(
            identifiers={("myfund", config_entry.entry_id)},
            name=f"MyFund {config_entry.data['wallet_name']}",
            manufacturer="MyFund.pl",
        )

    @property
    def native_value(self):
        if self.coordinator.data:
            value = self.coordinator.data.get("portfel", {}).get(self.field_key)
            if isinstance(value, str):
                return float(value.replace("+", ""))
            return value
        return None

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success
