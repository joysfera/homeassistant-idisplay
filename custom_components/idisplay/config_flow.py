import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, CONF_USER_LOGIN

_LOGGER = logging.getLogger(__name__)

class IDisplayConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for iDisplay."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate user input
            if not user_input[CONF_USER_LOGIN]:
                errors["base"] = "no_login_provided"
            else:
                return self.async_create_entry(title="iDisplay", data=user_input)

        # Build the form schema
        schema = vol.Schema({
            vol.Required(CONF_USER_LOGIN, description={"suggested_value": self.config_entry.data.get(CONF_USER_LOGIN, "")}): str,
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
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        errors = {}

        if user_input is not None:
            # Validate user input
            if not user_input[CONF_USER_LOGIN]:
                errors["base"] = "no_login_provided"
            else:
                return self.async_create_entry(title="", data=user_input)

        # Build the form schema
        schema = vol.Schema({
            vol.Required(CONF_USER_LOGIN, default=self.config_entry.data[CONF_USER_LOGIN]): str,
        })

        return self.async_show_form(
            step_id="init",
            data_schema=schema,
            errors=errors,
        )
