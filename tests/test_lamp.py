"""Tests for lamp."""

from lamp import Lamp
from consts import __version__
from unittest import mock
from dali.address import Short
import pytest
import json
from slugify import slugify

MIN_BRIGHTNESS = 2
MAX_BRIGHTNESS = 250


@pytest.fixture
def fake_driver():
    drive = mock.Mock()
    drive.send = lambda x: 0x00
    yield drive


@pytest.fixture
def fake_address():
    address = mock.Mock()
    address.address = 1

    address.__repr__ = lambda: "1"

def test_ha_config(fake_driver, fake_address):

    friendly_name = "my lamp"
    addr_number = 1
    addr = Short(1)

    lamp1 = Lamp(
        log_level="debug",
        driver=fake_driver,
        friendly_name=friendly_name,
        short_address=addr,
        min_physical_level=2,
        min_level=MIN_BRIGHTNESS,
        level=100,
        max_level=MAX_BRIGHTNESS,
    )

    assert lamp1.device_name == slugify(friendly_name)
    assert lamp1.short_address.address == addr_number

    assert str(lamp1) == f'my-lamp - address: {addr_number}, actual brightness level: 100 (minimum: {MIN_BRIGHTNESS}, max: {MAX_BRIGHTNESS}, physical minimum: 2)'

    assert json.loads(lamp1.gen_ha_config("test")) == {
        "name": friendly_name,
        "obj_id": "dali_light_my-lamp",
        "uniq_id": f"Mock_{addr}",
        "stat_t": "test/my-lamp/light/status",
        "cmd_t": "test/my-lamp/light/switch",
        "pl_off": "OFF",
        "bri_stat_t": "test/my-lamp/light/brightness/status",
        "bri_cmd_t": "test/my-lamp/light/brightness/set",
        "bri_scl": MAX_BRIGHTNESS,
        "on_cmd_type": "brightness",
        "avty_t": "test/status",
        "pl_avail": "online",
        "pl_not_avail": "offline",
        "device": {
            "ids": "dali2mqtt",
            "name": "DALI Lights",
            "sw": f"dali2mqtt {__version__}",
            "mdl": "Mock",
            "mf": "dali2mqtt",
        },
    }