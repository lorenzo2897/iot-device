from machine import I2C
import utime


class RGB:
	TCS34725_ADDRESS = 0x29            # I2C address of chip
	TCS34725_COMMAND_BITMASK = 0x80    # MSB = 1 for commands

	integration_time = 0
	gain = 0

	def __init__(self, sda, scl, led):
		self.__led = led
		# initialise the I2C port
		self.__i2c = I2C(scl=scl, sda=sda, freq=100000)

	def __write8(self, reg, value):
		# tells the chip where to write
		command = (self.TCS34725_COMMAND_BITMASK | reg) & 0xFF
		# tells the chip the value to write
		value = value & 0xFF
		# do it
		self.__i2c.writeto(self.TCS34725_ADDRESS, bytearray([command, value]))

	def __read8(self, reg):
		# tells the chip where to read
		command = (self.TCS34725_COMMAND_BITMASK | reg) & 0xFF
		self.__i2c.writeto(self.TCS34725_ADDRESS, bytearray([command]))
		# read a byte
		data = self.__i2c.readfrom(self.TCS34725_ADDRESS, 1)
		return int.from_bytes(data, 'little')

	def __read16(self, reg):
		# tells the chip where to read
		command = (self.TCS34725_COMMAND_BITMASK | reg) & 0xFF
		self.__i2c.writeto(self.TCS34725_ADDRESS, bytearray([command]))
		# read a byte
		data = self.__i2c.readfrom(self.TCS34725_ADDRESS, 2)
		return int.from_bytes(data, 'little')

	def enable(self):
		TCS34725_ENABLE = 0x00       # ENABLE register
		TCS34725_ENABLE_AEN = 0x02   # RGBC Enable - Writing 1 actives the ADC, 0 disables it
		TCS34725_ENABLE_PON = 0x01   # Power on - Writing 1 activates the internal oscillator, 0 disables it
		self.__write8(TCS34725_ENABLE, TCS34725_ENABLE_PON)
		utime.sleep_ms(3)
		self.__write8(TCS34725_ENABLE, TCS34725_ENABLE_PON | TCS34725_ENABLE_AEN)

	def disable(self):
		TCS34725_ENABLE = 0x00       # ENABLE register
		self.__write8(TCS34725_ENABLE, 0)

	def begin(self, integration_time=50, gain=4):
		# check that we are connected successfully
		TCS34725_ID = 0x12
		reportedID = self.__read8(TCS34725_ID)
		if reportedID != 0x44 and reportedID != 0x10:
			return False

		# set parameters
		self.set_integration_time(integration_time)
		self.set_gain(gain)
		self.enable()

		return True

	def set_integration_time(self, t):
		times = {
			2: 0xFF,
			24: 0xF6,
			50: 0xEB,
			101: 0xD5,
			154: 0xC0,
			700: 0x00
		}
		if t not in times:
			return False

		self.integration_time = t

		TCS34725_ATIME = 0x01  # Integration time register
		self.__write8(TCS34725_ATIME, times[t])

		return True

	def set_gain(self, g):
		gains = {
			1: 0x00,
			4: 0x01,
			16: 0x02,
			60: 0x03
		}
		if g not in gains:
			return False

		self.gain = g

		TCS34725_CONTROL = 0x0F  # Set the gain level for the sensor
		self.__write8(TCS34725_CONTROL, gains[g])

		return True

	def read_color(self):
		# register addresses
		TCS34725_CDATA = 0x14
		TCS34725_RDATA = 0x16
		TCS34725_GDATA = 0x18
		TCS34725_BDATA = 0x1A

		# read color values
		c = self.__read16(TCS34725_CDATA)
		r = self.__read16(TCS34725_RDATA)
		g = self.__read16(TCS34725_GDATA)
		b = self.__read16(TCS34725_BDATA)

		# wait for integration time to elapse
		utime.sleep_ms(self.integration_time + 1)

		return c, r, g, b

	def set_led(self, state):
		if state:
			self.__led.on()
		else:
			self.__led.off()

