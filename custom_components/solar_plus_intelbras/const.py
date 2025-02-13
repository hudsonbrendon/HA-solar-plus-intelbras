"""Constants for solar_plus_intelbras."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "solar_plus_intelbras"
ATTRIBUTION = "Data provided by https://ens-server.intelbras.com.br/api/"
SOLAR_PLUS_INTELBRAS_API_URL = "https://ens-server.intelbras.com.br/api"
CONF_EMAIL = "email"
CONF_PLUS = "plus"
CONF_PLANT_ID = "plant_id"
