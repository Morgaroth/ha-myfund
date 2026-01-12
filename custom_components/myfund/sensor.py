"""Sensor platform for MyFund integration."""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.myfund.sensors import MyFundTotalValueSensor, MyFundDailyChangeSensor, MyFundPortfolioSensor, \
    MyFundChangeSensor, MyFundProfitSensor
from custom_components.myfund.update_coordinator import MyFundDataUpdateCoordinator

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
        MyFundPortfolioSensor(coordinator, config_entry),
        MyFundTotalValueSensor(coordinator, config_entry),
        MyFundDailyChangeSensor(coordinator, config_entry),
        MyFundProfitSensor(coordinator, config_entry),
        MyFundChangeSensor(coordinator, config_entry, "zmianaW", "weekly_change", "weekly"),
        MyFundChangeSensor(coordinator, config_entry, "zmiana2W", "2weekly_change", "2weekly"),
        MyFundChangeSensor(coordinator, config_entry, "zmianaM", "monthly_change", "monthly"),
        MyFundChangeSensor(coordinator, config_entry, "zmiana3M", "3monthly_change", "3monthly"),
        MyFundChangeSensor(coordinator, config_entry, "zmiana6M", "6monthly_change", "6monthly"),
        MyFundChangeSensor(coordinator, config_entry, "zmianaR", "yearly_change", "yearly"),
    ]

    async_add_entities(entities)
