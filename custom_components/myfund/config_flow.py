"""Config flow for MyFund integration."""
import logging
from json import JSONDecodeError

import aiohttp
import async_timeout
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)


class MyFundConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for MyFund."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return MyFundOptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            _LOGGER.info(
                f"Received user input: wallet_name={user_input.get('wallet_name')}, api_key={'*' * len(user_input.get('api_key', ''))}")

            # Validate API key and wallet
            try:
                await self._test_credentials(
                    user_input["api_key"],
                    user_input["wallet_name"]
                )
                _LOGGER.info("Creating config entry after successful validation")
                return self.async_create_entry(
                    title=f"MyFund - {user_input['wallet_name']}",
                    data=user_input
                )
            except Exception as e:
                _LOGGER.error(f"Credential validation failed: {e}")
                errors["base"] = "invalid_auth"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("wallet_name"): str,
                vol.Required("api_key"): vol.All(str, vol.Length(min=1)),
                vol.Optional("update_interval", default=5): selector.NumberSelector(
                    selector.NumberSelectorConfig(min=5, mode=selector.NumberSelectorMode.BOX)
                ),
            }),
            errors=errors
        )

    async def _test_credentials(self, api_key: str, wallet_name: str):
        """Test if credentials are valid."""
        url = f"https://myfund.pl/API/v1/getPortfel.php?portfel={wallet_name}&apiKey={api_key}&format=json"

        _LOGGER.info(f"Testing MyFund API with URL: {url}")

        async with aiohttp.ClientSession() as session:
            with async_timeout.timeout(10):
                async with session.get(url) as response:
                    _LOGGER.info(f"API Response status: {response.status}")
                    _LOGGER.info(f"API Response headers: {response.headers}")

                    response_text = await response.text()
                    _LOGGER.info(f"API Response text: {response_text[:500]}")

                    try:
                        # Parse JSON manually since server returns wrong content-type
                        import json
                        data = json.loads(response_text)
                        _LOGGER.info(f"API Response JSON: {data}")

                        if str(data.get("status", {}).get("code")) == "1":
                            _LOGGER.error(f"API returned error: {data.get('status', {}).get('text')}")
                            raise Exception("Invalid credentials")

                        _LOGGER.info("API credentials validation successful")
                    except JSONDecodeError as e:
                        _LOGGER.error(f"Failed to parse JSON response: {e}")
                        raise Exception("Invalid credentials")


class MyFundOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle MyFund options."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        _LOGGER.debug("Options flow initialized for entry: %s", config_entry.entry_id)

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        _LOGGER.debug("Options step_init called with user_input: %s", user_input)
        _LOGGER.debug("Current config_entry.data: %s", self.config_entry.data)
        _LOGGER.debug("Current config_entry.options: %s", self.config_entry.options)
        
        if user_input is not None:
            _LOGGER.debug("Saving options: %s", user_input)
            return self.async_create_entry(title="", data=user_input)

        current_interval = self.config_entry.options.get("update_interval") or self.config_entry.data.get("update_interval", 5)
        _LOGGER.debug("Showing options form with current interval: %s", current_interval)
        
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(
                    "update_interval",
                    default=current_interval
                ): selector.NumberSelector(
                    selector.NumberSelectorConfig(min=5, mode=selector.NumberSelectorMode.BOX)
                ),
            })
        )
