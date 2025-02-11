[![Lint](https://github.com/hudsonbrendon/HA-solar-plus-intelbras/actions/workflows/lint.yml/badge.svg)](https://github.com/hudsonbrendon/HA-solar-plus-intelbras/actions/workflows/lint.yml)
[![Validate](https://github.com/hudsonbrendon/HA-solar-plus-intelbras/actions/workflows/validate.yml/badge.svg)](https://github.com/hudsonbrendon/HA-solar-plus-intelbras/actions/workflows/validate.yml)


# HomeAssistant Solar plus Intelbras

![logo](logo.png)

## Installation

Copy contents of custom_components/solar_plus_intelbras/ to custom_components/solar_plus_intelbras/ in your Home Assistant config folder.

## Installation using HACS

HACS is a community store for Home Assistant. You can install [HACS](https://github.com/custom-components/hacs) and then install Solar Plus Intelbras from the HACS store.

## Requirements

### Authentication

To authenticate, use the same email used at [https://solarplus.intelbras.com.br/](https://solarplus.intelbras.com.br/) and the token named "plus," which can be captured in any request in your browser’s network tab, for example:

![example](plus.png)

## Usage

Add inversors via Integrations (search for `Solar Plus Intelbras`) in Home Assistant UI. You can also simply click the button below if you have MyHomeAssistant redirects set up.

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=solar_plus_intelbras)

## Quick Start

This custom component creates the following sensors:

- Energy Today
- Today Economy
- Energy Total
- Total Economy
- Current Power
- Economy of Last 30 Days
- Year Economy
- Energy of Last 30 Days
- Saved Co2
- Saved Trees
- Saved Coal
- Inverters
- Dataloggers
- Alerts
- Today Alerts
- Price
- Capacity Installed
- Modules Amount
- Status
- Offgrid
- Last Record

# Disclaimer

a intelbras não disponibiliza API oficial, as informações são oriundas da api utilizada no sistema oficial utilizado pela plataforma web e mobile, a integração é baseada na biblioteca [https://github.com/hudsonbrendon/python-solar-plus-intelbras](https://github.com/hudsonbrendon/python-solar-plus-intelbras) podendo haver indisponibilidade e bloqueio da API