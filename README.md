# MyFund Home Assistant Integration

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Morgaroth&repository=ha-myfund&category=integration)

A Home Assistant custom integration for tracking MyFund.pl portfolio data.

## Mirror Notice

**Note:** If you're viewing this on GitHub, this is a mirror repository. The parent repository is hosted on [GitLab](https://gitlab.com/mateuszjaje/ha-myfund).

## Features

- Track portfolio total value in PLN
- Configurable update intervals (5-60 minutes)
- Secure API key storage
- Multiple portfolio support

## Installation

### HACS (Recommended)

1. Click the badge above or manually add this repository to HACS
2. Install "MyFund" integration
3. Restart Home Assistant
4. Add integration through UI: Settings > Devices & Services > Add Integration > MyFund

### Manual Installation

1. Copy `custom_components/myfund` to your Home Assistant `custom_components` directory
2. Restart Home Assistant
3. Add the integration through the UI

## Configuration

1. Get your API key from MyFund.pl (Menu > Account > Account Settings > API Key)
2. Add integration with:
   - **Portfolio Name**: Your portfolio name from MyFund.pl
   - **API Key**: Your generated API key
   - **Update Interval**: How often to fetch data (5-60 minutes)

## Sensors

- `sensor.myfund_[portfolio_name]_total_value`: Portfolio total value in PLN

## Testing

For development and testing, use the provided Docker Compose setup:

```bash
docker-compose up -d
```

This starts a Home Assistant instance with the integration pre-loaded. Access it at `http://localhost:8123`.
To test, you need to first open the HomeAssistant UI and create an account. Then configure testing instance 
of your integration.

## API Information

This integration uses the MyFund.pl API which caches data for 5 minutes. Setting update intervals below 5 minutes won't provide fresher data.