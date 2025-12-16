import unittest
import mock.GPIO as GPIO
from unittest.mock import patch, PropertyMock
from unittest.mock import Mock

from mock.adafruit_bmp280 import Adafruit_BMP280_I2C
from src.smart_room import SmartRoom
from mock.senseair_s8 import SenseairS8


class TestSmartRoom(unittest.TestCase):

    @patch.object(GPIO, "input")
    def test_occupancy_yes(self, mock_infrared_sensor: Mock):
        mock_infrared_sensor.return_value = True
        room = SmartRoom()
        outcome = room.check_room_occupancy()
        self.assertTrue(outcome)

