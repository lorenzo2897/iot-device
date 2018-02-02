from machine import Pin
from sensors.servo import Servo
from sensors.rgb import RGB
from sensors.temperature import Temperature

import uasyncio as asyncio

class Tea:
	def __init__(self):
		self.concentration = 0.50
		self.temperature = 80
		self.state = 'ready'
		self.rgb = RGB(sda=Pin(4), scl=Pin(5), led=Pin(16, Pin.OUT))
		self.temp = Temperature(sda=Pin(4), scl=Pin(5))
		self.servo = Servo(Pin(12))

	def stats(self):
		print("stats requested")

		self.rgb.begin()

		tea_concentration, _, _, _ = self.rgb.read_color()
		water_temperature = self.temp.read_temperature()

		data = {
			"state": self.state,
			"water_temperature": water_temperature,
			"tea_concentration": tea_concentration
		}

		return data

	async def make_tea(self):
		while True:
			print("started")
			await asyncio.sleep(5)

		self.state = 'boiling_water'

		#start heating, wait until boiling

		self.state = 'pumping_water'

		#pump water into cup

		#lower tea-bag

		self.state = 'dissolving'

		#remove tea-bag when concentration wanted is obtained

		self.state = 'cooling'

		#wait until temperature wanted is obtained and notify user when done

		self.state = 'done'

	def abort(self):
		print("aborted")

	def update_settings(self, settings):
		self.temperature = settings['temperature']
		self.concentration = settings['concentration']