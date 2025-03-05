"""Constants for solar_plus_intelbras."""

import datetime
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "solar_plus_intelbras"
ATTRIBUTION = "Data provided by https://ens-server.intelbras.com.br/api/"
SOLAR_PLUS_INTELBRAS_API_URL = "https://ens-server.intelbras.com.br/api"
CONF_EMAIL = "email"
CONF_PLUS = "plus"
CONF_PLANT_ID = "plant_id"
NOTIFICATION_ID_FORMAT = "solar_plus_intelbras"
NOTIFICATION_TITLE_DEFAULT = "Solar Plus Intelbras Alert"

ATTR_MESSAGE = "message"
ATTR_TITLE = "title"
ATTR_NOTIFICATION_ID = "notification_id"
ATTR_PRIORITY = "priority"

PRIORITY_NORMAL = "normal"
PRIORITY_CRITICAL = "critical"
PRIORITY_WARNING = "warning"
PRIORITY_INFO = "info"

DEFAULT_NOTIFICATION_CHECK_INTERVAL = datetime.timedelta(minutes=30)
