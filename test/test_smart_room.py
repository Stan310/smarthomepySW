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

    @patch.object(GPIO,"input")
    def test_occupancy_no(self, mock_infrared_sensor: Mock):
        mock_infrared_sensor.return_value = False
        room = SmartRoom()
        outcome = room.check_room_occupancy()
        self.assertFalse(outcome)

    @patch.object(GPIO, "input")
    def test_enough_light_yes(self, mock_photoresistor: Mock):
        mock_photoresistor.return_value = True
        room = SmartRoom()
        outcome = room.check_enough_light()
        self.assertTrue(outcome)

    @patch.object(GPIO, "input")
    def test_enough_light_no(self, mock_photoresistor: Mock):
        mock_photoresistor.return_value = False
        room = SmartRoom()
        outcome = room.check_enough_light()
        self.assertFalse(outcome)


    @patch.object(GPIO, "output")
    @patch.object(SmartRoom, "check_enough_light")
    @patch.object(SmartRoom, "check_room_occupancy")
    def test_person_in_room_not_enough_light(self, mock_infrared_sensor: Mock, mock_photoresistor: Mock, mock_led: Mock):
        mock_infrared_sensor.return_value = True
        mock_photoresistor.return_value = False
        room = SmartRoom()
        room.manage_light_level()
        mock_led.assert_called_once_with(room.LED_PIN, True)
        self.assertTrue( room.light_on)

    @patch.object(GPIO, "output")
    @patch.object(SmartRoom, "check_enough_light")
    @patch.object(SmartRoom, "check_room_occupancy")
    def test_person_in_room_enough_light(self, mock_infrared_sensor: Mock, mock_photoresistor: Mock, mock_led: Mock):
        mock_infrared_sensor.return_value = True
        mock_photoresistor.return_value = True
        room = SmartRoom()
        room.manage_light_level()
        mock_led.assert_called_once_with(room.LED_PIN, False)
        self.assertFalse(room.light_on)

    @patch.object(GPIO, "output")
    @patch.object(SmartRoom, "check_enough_light")
    @patch.object(SmartRoom, "check_room_occupancy")
    def test_person_in_room_enough_light(self, mock_infrared_sensor: Mock, mock_photoresistor: Mock,
                                             mock_led: Mock):
        mock_infrared_sensor.return_value = True
        mock_photoresistor.return_value = True
        room = SmartRoom()
        room.manage_light_level()
        mock_led.assert_called_once_with(room.LED_PIN, False)
        self.assertTrue(room.light_on)

    @patch.object(GPIO, "output")
    @patch.object(SmartRoom, "check_enough_light")
    @patch.object(SmartRoom, "check_room_occupancy")
    def test_no_person_in_room_enough_light(self, mock_infrared_sensor: Mock, mock_photoresistor: Mock, mock_led: Mock):
        mock_infrared_sensor.return_value = False
        mock_photoresistor.return_value = True
        room = SmartRoom()
        room.manage_light_level()
        mock_led.assert_called_once_with(room.LED_PIN, True)
        self.assertFalse(room.light_on)

    @patch.object(GPIO, "output")
    @patch.object(SmartRoom, "check_enough_light")
    @patch.object(SmartRoom, "check_room_occupancy")
    def test_no_person_in_room_not_enough_light(self, mock_infrared_sensor: Mock, mock_photoresistor: Mock, mock_led: Mock):
        mock_infrared_sensor.return_value = False
        mock_photoresistor.return_value = False
        room = SmartRoom()
        room.manage_light_level()
        mock_led.assert_called_once_with(room.LED_PIN, False)
        self.assertFalse(room.light_on)

    @patch.object(Adafruit_BMP280_I2C, "temperature", new_callable=PropertyMock)
    @patch.object(SmartRoom, "change_servo_angle")
    def test_manage_window_open_window_low_bound(self, mock_servo: Mock, mock_temperature_sensor: Mock):
        mock_temperature_sensor.side_effect = [18, 20.1]
        sut = SmartRoom()
        sut.manage_window()
        mock_servo.assert_called_once_with(12)
        self.assertTrue(sut.window_open)
