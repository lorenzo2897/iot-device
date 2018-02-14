from machine import Pin
from drivers.servo import Servo
from drivers.rgb import RGB
from drivers.infrared import Infrared

import uasyncio as asyncio


class Tea:
	send_push = None

	__SERVO_LOWERED = 0.60
	__SERVO_RAISED = 0.36

	def __init__(self):
		self.concentration = 0.50
		self.temperature = 80
		self.state = 'ready'
		self.rgb = RGB(sda=Pin(4), scl=Pin(5), led=Pin(2, Pin.OUT))
		self.boiler_temp = Infrared(sda=Pin(4), scl=Pin(5), addr=0x41, samplerate=4)  # A0 = 1, A1 = 0
		self.tea_temp = Infrared(sda=Pin(4), scl=Pin(5), addr=0x45, samplerate=4)  # A0 = 1, A1 = 1
		self.servo = Servo(Pin(12))
		self.boiler = Pin(14, Pin.OUT)
		self.pump = Pin(15, Pin.OUT)

		self.rgb.begin()
		self.rgb.set_led(0)
		self.boiler.off()
		self.pump.off()
		self.servo.sweep(self.__SERVO_RAISED)

	def stats(self):
		print("sending stats")

		tea_concentration, _, _, _ = self.rgb.read_color()
		boiler_temperature = self.boiler_temp.get_obj_temperature()
		tea_temperature = self.tea_temp.get_obj_temperature()

		data = {
			"state": self.state,

			"settings_temperature": self.temperature,
			"settings_concentration": self.concentration,

			"boiler_temperature": boiler_temperature,
			"tea_temperature": tea_temperature,
			"tea_concentration": tea_concentration,
			"servo_position": self.servo.get_position()
		}

		return data

	async def make_tea(self):
		print("started")
		self.boiler.off()
		self.pump.off()
		self.rgb.set_led(0)
		self.servo.set_position(self.__SERVO_RAISED)

		# ============== start heating, wait until boiling ==============
		self.state = 'boiling'
		self.send_push(self.stats())

		self.boiler.on()
		await asyncio.sleep(4)
		self.boiler.off()

		# ===================== pump water into cup =====================
		if self.state == 'aborting':
			self.reset_all()
			return
		self.state = 'pumping'
		self.send_push(self.stats())

		self.pump.on()
		await asyncio.sleep(4)
		self.pump.off()

		# ======================== lower tea-bag ========================
		if self.state == 'aborting':
			self.reset_all()
			return
		self.state = 'lowering'
		self.send_push(self.stats())

		self.servo.sweep(self.__SERVO_LOWERED)
		await asyncio.sleep(2)

		# =============== wait for correct concentration ================
		if self.state == 'aborting':
			self.reset_all()
			return
		self.state = 'brewing'
		self.send_push(self.stats())

		self.rgb.set_led(1)
		await asyncio.sleep(4)
		self.rgb.set_led(0)

		# ======================= remove tea-bag ========================
		if self.state == 'aborting':
			self.reset_all()
			return
		self.state = 'raising'
		self.send_push(self.stats())

		self.servo.sweep(self.__SERVO_RAISED)
		await asyncio.sleep(2)

		# ========== wait until temperature wanted is obtained ==========
		if self.state == 'aborting':
			self.reset_all()
			return
		self.state = 'cooling'
		self.send_push(self.stats())

		await asyncio.sleep(4)

		# ==================== notify user when done ====================
		self.state = 'done'
		stats = self.stats()
		stats["notify"] = True
		self.send_push(stats)

	def abort(self):
		if self.state == 'done':
			self.reset_all()
			self.state = 'ready'
		else:
			self.state = 'aborting'
			print("aborting")

	def update_settings(self, settings):
		self.temperature = settings['temperature']
		self.concentration = settings['concentration']

	def reset_all(self):
		# make sure everything is off and back where it should be
		self.boiler.off()
		self.pump.off()
		self.rgb.set_led(0)
		self.servo.sweep(self.__SERVO_RAISED)
		self.state = 'ready'
		self.send_push(self.stats())
		print("ready")
