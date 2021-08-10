from __future__ import annotations
import logging
import requests

from .const import DOMAIN
from . import HasgSwitch
import voluptuous as vol
from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers import (
    config_validation as cv,
    device_registry,
    entity_platform,
)

_LOGGER = logging.getLogger(__name__)

from homeassistant.const import (
    CONF_HOST,
    CONF_PORT,
    CONF_SSL,
)

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


from homeassistant.components.switch import (
    DEVICE_CLASS_OUTLET,
    DEVICE_CLASS_SWITCH,
    SwitchEntity,
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    _LOGGER.warning("adding device, %s ", hass.data[DOMAIN])

    coordinator = hass.data[DOMAIN]
    scheme = "http"
    # connected = False
    _LOGGER.warning(
        "hass: %s , config: %s , add_ent: %s, disc: %s",
        hass,
        config,
        add_entities,
        discovery_info,
    )

    host = coordinator["config"]["host"]
    port = coordinator["config"]["port"]
    ssl = coordinator["config"]["ssl"]
    # _LOGGER.warning("host: %s , port: %s , ssl: %s ", host, port, ssl)

    if ssl:
        scheme = "https"
    switches = []

    req_url = scheme + "://" + host + ":" + str(port) + "/getjson"

    try:
        r = requests.get(req_url)
        if r.status_code == 200:
            # connected = True
            # _LOGGER.warning(r.status_code)
            # _LOGGER.warning(r.json())

            for site in r.json():
                for device in site["devices"]:
                    # _LOGGER.warning(device)
                    custom = device
                    custom["scheme"] = scheme
                    custom["host"] = host
                    custom["port"] = port
                    switch = HasgSwitch(device)
                    switches.append(switch)
                add_entities(switches, True)

        else:
            message = (
                "Unable to connect to Smart Grade container ("
                + str(r.status_code)
                + ")"
            )
            _LOGGER.error(message)
            hass.components.persistent_notification.create(
                message,
                title="Smart grade error",
                notification_id="hasmartgrade_err",
            )
    except requests.RequestException as e:
        _LOGGER.error("Error: %s ", e)
        # _LOGGER.info(e)
        # raise SystemExit(e)
        message = "Unable to connect to Smart Grade container"
        hass.components.persistent_notification.create(
            message,
            title="Smart grade error",
            notification_id="hasmartgrade_err",
        )
