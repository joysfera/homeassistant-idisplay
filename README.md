# Home Assistant integration for [iDisplay](https://idisplej.cz/)

Just install it, configure with your login name and that's it.

Get your iDisplay or WiFi Display at [iDisplay.cz](https://idisplej.cz/)

<img src="https://idisplej.cz/assets/cidla.jpg" width=300 alt="iDisplay">

# Installation

### via HACS (Recommended)

Either click on this button
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=joysfera&repository=homeassistant-idisplay&category=integration)  or follow the steps below:

1. Open Home Assistant
2. Go to **HACS** → **Integrations**
3. Open the three-dot menu
4. Choose **Custom repositories**
5. Add this repository URL
6. Set category to **Integration**
7. Search for "**iDisplay**" and install it
8. Restart Home Assistant
9. Go to **Settings** → **Devices & Services**, click **Add Integration** and select **iDisplay**

### Manual

1. Copy `custom_components/idisplay/` to your Home Assistant's `custom_components/` directory
2. Restart Home Assistant
3. Go to **Settings** → **Devices & Services**, click **Add Integration** and select **iDisplay**

# Configuration

When the iDisplay integration asks, enter there your Teploty.info login name
