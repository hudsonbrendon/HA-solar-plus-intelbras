from homeassistant.helpers.device_registry import DeviceInfo


class InverterDevice:
    """Representation of an Inverter device."""

    def __init__(self, identifier: str, name: str) -> None:
        """Initialize the inverter device."""
        self._identifier = identifier
        self._name = name

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information about this inverter."""
        return DeviceInfo(
            identifiers={(self._identifier,)},
            name=self._name,
            manufacturer="Intelbras",
            model="Inverter",
        )


class DataloggerDevice:
    """Representation of a Datalogger device."""

    def __init__(self, identifier: str, name: str) -> None:
        """Initialize the datalogger device."""
        self._identifier = identifier
        self._name = name

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information about this datalogger."""
        return DeviceInfo(
            identifiers={(self._identifier,)},
            name=self._name,
            manufacturer="Intelbras",
            model="Datalogger",
        )
