import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, CONF_USER_LOGIN

_LOGGER = logging.getLogger(__name__)

class IDisplayConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for iDisplay."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            login = user_input.get(CONF_USER_LOGIN, "").strip()
            if not login:
                errors[CONF_USER_LOGIN] = "no_login_provided"
            else:
                await self.async_set_unique_id(login)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=login,
                    data={CONF_USER_LOGIN: login},
                )

        schema = vol.Schema({
            vol.Required(CONF_USER_LOGIN): str,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return IDisplayOptionsFlow(config_entry)


class IDisplayOptionsFlow(config_entries.OptionsFlow):
    """Handle an options flow for iDisplay."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self._config_entry = config_entry  # Use private attribute to avoid conflict with HA base property

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        errors = {}

        if user_input is not None:
            login = user_input.get(CONF_USER_LOGIN, "").strip()
            if not login:
                errors[CONF_USER_LOGIN] = "no_login_provided"
            else:
                return self.async_create_entry(title="", data={CONF_USER_LOGIN: login})

        current_login = self._config_entry.options.get(
            CONF_USER_LOGIN,
            self._config_entry.data.get(CONF_USER_LOGIN, "")
        )

        schema = vol.Schema({
            vol.Required(CONF_USER_LOGIN, default=current_login): str,
        })

        return self.async_show_form(
            step_id="init",
            data_schema=schema,
            errors=errors,
        )
