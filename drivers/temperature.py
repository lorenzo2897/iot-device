from machine import I2C
import utime


class Temperature:
	SI7021_ADDRESS = 0x40

	def __init__(self, sda, scl):
		# initialise the I2C port
		self.__i2c = I2C(scl=scl, sda=sda, freq=100000)

	def __write8(self, reg, value):
		command = reg & 0xFF  # tells the chip where to write
		value = value & 0xFF  # tells the chip the value to write
		self.__i2c.writeto(self.SI7021_ADDRESS, bytearray([command, value]))

	def __read8(self, reg):
		# tells the chip where to read
		command = reg & 0xFF
		self.__i2c.writeto(self.SI7021_ADDRESS, bytearray([command]))
		# read a byte
		data = self.__i2c.readfrom(self.SI7021_ADDRESS, 1)
		return int.from_bytes(data, 'little')

	def __read16(self, reg):
		# tells the chip where to read
		command = reg & 0xFF
		self.__i2c.writeto(self.SI7021_ADDRESS, bytearray([command]))
		# read a byte
		data = self.__i2c.readfrom(self.SI7021_ADDRESS, 2)
		return int.from_bytes(data, 'little')

	def reset(self):
		SI7021_RESET_CMD = 0xFE
		self.__i2c.writeto(self.SI7021_ADDRESS, bytearray([SI7021_RESET_CMD]))
		utime.sleep_ms(50)

	def read_temperature(self):
		# send temperature read command
		SI7021_MEASTEMP_NOHOLD_CMD = 0xF3
		self.__i2c.writeto(self.SI7021_ADDRESS, bytearray([SI7021_MEASTEMP_NOHOLD_CMD]))
		utime.sleep_ms(25)
		# read a byte
		data = self.__i2c.readfrom(self.SI7021_ADDRESS, 2)
		temperature_code = int.from_bytes(data, 'big')

		temp = 175.72 * float(temperature_code) / 65536 - 46.85
		return temp
