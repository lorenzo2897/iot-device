from machine import Pin
from sensors.servo import Servo
from sensors.rgb import RGB
from sensors.temperature import Temperature

import uasyncio as asyncio


class Tea:
	send_push = None

	def __init__(self):
		self.concentration = 0.50
		self.temperature = 80
		self.state = 'ready'
		self.rgb = RGB(sda=Pin(4), scl=Pin(5), led=Pin(16, Pin.OUT))
		self.temp = Temperature(sda=Pin(4), scl=Pin(5))
		self.servo = Servo(Pin(12))

		self.rgb.begin()

	def stats(self):
		print("sending stats")

		tea_concentration, _, _, _ = self.rgb.read_color()
		water_temperature = self.temp.read_temperature()

		data = {
			"state": self.state,

			"settings_temperature": self.temperature,
			"settings_concentration": self.concentration,

			"boiler_temperature": 0,
			"tea_temperature": water_temperature,
			"tea_concentration": tea_concentration,
			"servo_position": self.servo.get_position()
		}

		return data

	async def make_tea(self):
		print("started")

		# start heating, wait until boiling
		self.state = 'boiling'
		self.send_push(self.stats())

		await asyncio.sleep(4)

		# pump water into cup
		if self.state == 'aborting':
			self.reset_all()
			return
		self.state = 'pumping'
		self.send_push(self.stats())

		await asyncio.sleep(4)

		# lower tea-bag
		if self.state == 'aborting':
			self.reset_all()
			return
		self.state = 'lowering'
		self.send_push(self.stats())

		await asyncio.sleep(4)

		# wait for correct concentration
		if self.state == 'aborting':
			self.reset_all()
			return
		self.state = 'brewing'
		self.send_push(self.stats())

		await asyncio.sleep(4)

		# remove tea-bag
		if self.state == 'aborting':
			self.reset_all()
			return
		self.state = 'raising'
		self.send_push(self.stats())

		await asyncio.sleep(4)

		# wait until temperature wanted is obtained
		if self.state == 'aborting':
			self.reset_all()
			return
		self.state = 'cooling'
		self.send_push(self.stats())

		await asyncio.sleep(4)

		# notify user when done
		self.state = 'done'
		self.send_push(self.stats())

	def abort(self):
		if self.state == 'done':
			self.reset_all()
		else:
			self.state = 'aborting'
			print("aborting")

	def update_settings(self, settings):
		self.temperature = settings['temperature']
		self.concentration = settings['concentration']

	def reset_all(self):
		# make sure everything is off and back where it should be
		self.state = 'ready'
		self.send_push(self.stats())
		print("ready")
