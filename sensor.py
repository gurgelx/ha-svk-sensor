"""Platform for sensor integration."""
from homeassistant.helpers.entity import Entity
import requests
import time
import json


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    add_entities([SVKSensor()])


class SVKSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self):
        """Initialize the sensor."""
        self._state = None
        self.currentHz = 0
        self.measurements = []
        self.next_update = 0

    def poll_svk(self):
        ticks = int(time.time() - 900)
        url = "https://www.svk.se/services/statnett/v1/frequency/bysecondwithxy?frominticks=" + \
            str(ticks)
        r = requests.get(url)
        data = json.loads(r.text)
        self.measurements = data['Measurements']
        self.currentHz = float(self.measurements[-1][1])

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Svenska kraftnät'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "Hz"

    @property
    def measurements(self):
        """Returns the measurements."""
        return self.measurements

    def update(self):
        """Fetch new state data for the sensor."""
        if self.next_update < time.time():
            self.poll_svk()
            self.next_update = time.time() + 300  # schedule next update in 5 min

        self._state = self.currentHz
