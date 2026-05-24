![hacs_badge](https://img.shields.io/badge/hacs-custom-orange.svg)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)
[![Lint](https://github.com/hudsonbrendon/HA-solar-plus-intelbras/actions/workflows/lint.yml/badge.svg)](https://github.com/hudsonbrendon/HA-solar-plus-intelbras/actions/workflows/lint.yml)
[![Validate](https://github.com/hudsonbrendon/HA-solar-plus-intelbras/actions/workflows/validate.yml/badge.svg)](https://github.com/hudsonbrendon/HA-solar-plus-intelbras/actions/workflows/validate.yml)


# Home Assistant Solar plus Intelbras

![logo](logo.png)

# Install

### Installation via HACS

Have HACS installed, this will allow you to update easily.

Adding Solar Plus Intelbras to HACS can be using this button:

[![image](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=hudsonbrendon&repository=HA-solar-plus-intelbras&category=integration)

If the button above doesn't work, add `https://github.com/hudsonbrendon/HA-solar-plus-intelbras` as a custom repository of type Integration in HACS.

- Click Install on the `Solar Plus Intelbras` integration.
- Restart the Home Assistant.

### Manual installation

- Copy `solar_plus_intelbras`  folder from [latest release](https://github.com/hudsonbrendon/HA-solar-plus-intelbras/releases/latest) to your `<config dir>/custom_components/` directory.
- Restart the Home Assistant.

## Configuration

Adding Solar Plus Intelbras to your Home Assistant instance can be done via the UI using this button:

[![image](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start?domain=solar_plus_intelbras)

### Manual Configuration

If the button above doesn't work, you can also perform the following steps manually:

* Navigate to your Home Assistant instance.
* In the sidebar, click Settings.
* From the Setup menu, select: Devices & Services.
* In the lower right corner, click the Add integration button.
* In the list, search and select `Solar Plus Intelbras`.
* Follow the on-screen instructions to complete the setup.

## Authentication

To authenticate, use the same email used at [https://solarplus.intelbras.com.br/](https://solarplus.intelbras.com.br/) and the token named "plus," which can be captured in any request in your browser’s network tab, for example:

![plus](plus.png)

- your token "plus".

You only need the email and the "plus" token. After validating them, the integration lists the plants on your account and you pick which one to add — so you can add several plants (one config entry each). The plant ID no longer has to be entered by hand.

## Usage

Add inversors via Integrations (search for `Solar Plus Intelbras`) in Home Assistant UI. You can also simply click the button below if you have MyHomeAssistant redirects set up.

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=solar_plus_intelbras)

## Devices

This custom component creates the following devices:

### Inverter

![inverter](inverter.png)

### Datalogger

![datalogger](datalogger.png)

### Sensors

The integration creates three devices — **Plant**, **Inverter**, and **Datalogger** — and supports multiple inverters per plant.

**Plant:** Energy today / total / last 30 days / this year (kWh), Current power (W), Economy today / total / last 30 days / this year, CO2 / trees / coal saved, Energy price, Installed capacity, Modules, Plant status, Alerts, Alerts today, Weather temperature / humidity / condition.

**Inverter (per device):** Temperature (°C), Power (W), Energy today (kWh), Status, Serial number, Last record, Online (binary).

**Datalogger (per device):** Firmware version, MAC address, Signal strength (RSSI), Last record.

Monetary sensors use the currency reported by your account (e.g. `BRL`). The polling interval is configurable via the integration's **Configure** (options) dialog. The integration is available in English, Portuguese and Spanish.

### Energy Dashboard history

The energy sensors feed the Energy Dashboard automatically going forward. To **backfill past months**, call the `solar_plus_intelbras.import_history` service (optionally with `years`, default 2). It imports monthly generation as a long-term statistic per plant that you can add to the Energy Dashboard. Requires the `recorder` integration.

If your "plus" token rotates you'll be prompted to re-authenticate; you can also **Reconfigure** the entry to change the email/plus without removing it.

# How it works

The integration is **cloud polling**: it fetches data from the Solar Plus Intelbras API on a fixed interval (default 5 minutes, configurable via the integration's **Configure** dialog). Inverters and dataloggers are discovered automatically — new devices appear without a restart, and devices removed from your account are pruned.

**Use cases:** monitor live production and current power, track savings and environmental impact, follow per-inverter health/status, drive automations (e.g. notify when an inverter goes offline via the `solar_plus_intelbras.send_alert` service), and visualise generation in the Energy Dashboard.

**Known limitations:** Intelbras does not provide an official API, so availability and blocking are possible (see the Disclaimer). Historical statistics are imported at monthly granularity via `import_history`.

# Debugging

To enable debug for Solar Plus Intelbras integration, add following to your configuration.yaml:

```yml
logger:
  default: info
  logs:
    custom_components.solar_plus_intelbras: debug
```

# Disclaimer

Intelbras does not provide an official API, the information comes from the API used in the official system used by the web and mobile platform, the integration is based on the library [https://github.com/hudsonbrendon/python-solar-plus-intelbras](https://github.com/hudsonbrendon/python-solar-plus-intelbras) and there may be unavailability and blocking of the API.
