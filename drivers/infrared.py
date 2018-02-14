from machine import I2C


class Infrared:
	BASE_I2C_ADDRESS = 0x40
	__i2c_address = BASE_I2C_ADDRESS

	def __init__(self, sda, scl, addr=BASE_I2C_ADDRESS, samplerate=8):
		# initialise the I2C port
		self.__i2c = I2C(scl=scl, sda=sda, freq=100000)
		self.__i2c_address = addr
		self.set_rate(samplerate)

	def __read16(self, reg):
		# tells the chip where to read
		command = reg & 0xFF
		self.__i2c.writeto(self.__i2c_address, bytearray([command]))
		# read a byte
		data = self.__i2c.readfrom(self.__i2c_address, 2)
		return int.from_bytes(data, 'big')

	def __write16(self, reg, value):
		command = reg & 0xFF  # tells the chip where to write
		valueHi = (value >> 8) & 0xFF  # tells the chip the value to write
		valueLo = value & 0xFF
		self.__i2c.writeto(self.__i2c_address, bytearray([command, valueHi, valueLo]))

	def set_rate(self, rate):
		TMP007_CONFIG = 0x02
		TMP007_CFG_MODEON = 0x1000
		TMP007_CFG_TRANSC = 0x0040
		TMP007_CFG_SAMPLE = {1: 0x0000, 2: 0x0200, 4: 0x0400, 8: 0x0600, 16: 0x0800}
		self.__write16(TMP007_CONFIG, TMP007_CFG_MODEON | TMP007_CFG_TRANSC | TMP007_CFG_SAMPLE[rate])

	def get_die_temperature(self):
		TMP007_TDIE = 0x01
		raw = self.__read16(TMP007_TDIE) >> 2
		return raw * 0.03125

	def get_obj_temperature(self):
		TMP007_TOBJ = 0x03
		raw = self.__read16(TMP007_TOBJ)
		if raw & 0x1:
			return 0
		return (raw >> 2) * 0.03125

	past_temperatures = []

	def read_temperature(self):
		temp = max(self.get_obj_temperature(), self.get_die_temperature())
		if temp < 10 or temp > 101:
			return None
		else:
			self.past_temperatures.append(temp)
			self.past_temperatures = self.past_temperatures[-3:]
			return sum(self.past_temperatures) / len(self.past_temperatures)
