""" Smart grade component """
import logging
import re
from attr import attributes

import requests

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.helpers import discovery
from homeassistant.components.switch import SwitchEntity

# from homeassistant.helpers.entityfilter import FILTER_SCHEMA
# from homeassistant.components.switch import PLATFORM_SCHEMA, SwitchDevice

# from homeassistant.util import ssl as ssl_util


from homeassistant.const import (
    CONF_HOST,
    CONF_PORT,
    CONF_SSL,
)

from .const import (
    DOMAIN,
    PLATFORMS,
)


_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.All(
            cv.ensure_list,
            [
                vol.Schema(
                    {
                        vol.Required(CONF_HOST): cv.string,
                        vol.Required(CONF_PORT): cv.port,
                        vol.Optional(CONF_SSL, default=False): cv.boolean,
                    }
                )
            ],
        )
    },
    extra=vol.ALLOW_EXTRA,
)


def setup(hass, config):
    # _LOGGER.warning(config)

    for conf in config[DOMAIN]:
        if hass.data.get(DOMAIN) is None:
            hass.data[DOMAIN] = {
                "unique_ids": [],
                "entities": {},
                "oauth": {},
                "config": {
                    "host": conf[CONF_HOST],
                    "port": conf[CONF_PORT],
                    "ssl": conf[CONF_SSL],
                },
            }
    #     # _LOGGER.warning(conf)

    # # _LOGGER.info(hasg)
    for platform in PLATFORMS:
        # _LOGGER.warning("sending config: %s", config)
        discovery.load_platform(hass, platform, DOMAIN, {}, config)

    return True


class HasgSwitch(SwitchEntity):
    def __init__(self, device):
        """Initialize Smart grade switch"""
        # _LOGGER.warning("init device")
        # self._id = "id"
        # self._state = False
        # _LOGGER.warning("Devices: %s", device)
        self._device = device
        self._id = device["id"]
        # _LOGGER.warning("id: %s", self.unique_id)
        self._name = device["name"]
        # self.name = self._name
        self._description = device["description"]
        self._online = device["is_online"]
        self._fw = device["firmware"]
        self._switch = device["switch_1"]
        self._scheme = device["scheme"]
        self._host = device["host"]
        self._port = device["port"]

    def update(self):
        """Trigger update for all switches on the parent device."""
        # _LOGGER.warning("updating device")
        req_url = self._scheme + "://" + self._host + ":" + str(self._port) + "/getjson"
        try:
            r = requests.get(req_url)
            if r.status_code == 200:
                # _LOGGER.warning(r.status_code)
                # _LOGGER.warning(r.json())

                for device in r.json():
                    if device["id"] == self._id:
                        # _LOGGER.warning("updating %s", device["id"])
                        self._switch = device["switch_1"]

            else:
                _LOGGER.error("Error updating device: %s", self._id)
        except requests.RequestException as e:
            _LOGGER.error("Error updating device: %s", self._id)
            _LOGGER.error("Error: %s ", e)

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        req_url = (
            self._scheme
            + "://"
            + self._host
            + ":"
            + str(self._port)
            + "/toggle/"
            + self._id
            + "/switch_1/true"
        )
        try:
            r = requests.get(req_url)
            if r.status_code == 200:
                # _LOGGER.warning(r.status_code)
                # _LOGGER.warning(r.json())
                # _LOGGER.warning("Turrned on")
                self._switch = True
            else:
                _LOGGER.error("Error turning on device: %s", self._id)
        except requests.RequestException as e:
            _LOGGER.error("Error turning on device: %s", self._id)
            _LOGGER.error("Error: %s ", e)

    def turn_off(self, **kwargs):
        """Turn the switch off."""
        req_url = (
            self._scheme
            + "://"
            + self._host
            + ":"
            + str(self._port)
            + "/toggle/"
            + self._id
            + "/switch_1/false"
        )
        try:
            r = requests.get(req_url)
            if r.status_code == 200:
                # _LOGGER.warning(r.status_code)
                # _LOGGER.warning(r.json())
                # _LOGGER.warning("Turrned off")
                self._switch = False
            else:
                _LOGGER.error("Error turning on device: %s", self._id)
        except requests.RequestException as e:
            _LOGGER.error("Error turning on device: %s", self._id)
            _LOGGER.error("Error: %s ", e)

    @property
    def is_on(self):
        """Return true if device is on."""
        return self._switch

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self._id

    @property
    def name(self):
        """Return a unique ID."""
        return self._name

    @property
    def device_info(self):
        return {
            "identifiers": {
                # Serial numbers are unique identifiers within a specific domain
                (DOMAIN, self._id)
            },
            "name": self._name,
            "manufacturer": "SmartGrade",
            "model": "SmartGrade",
            "sw_version": self._fw,
        }

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        # attributes = {}
        # attributes["id"] = self._id
        attributes = self._device
        return attributes
