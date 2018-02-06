from umqtt.simple import MQTTClient
import uasyncio as asyncio
import ubinascii
import machine
import json


class IotClient:
	def __init__(self, ip, stats, make_tea, abort, update_settings):
		self.client = MQTTClient(ubinascii.hexlify(machine.unique_id()), ip)
		self.client.set_callback(self.callback)
		self.client.connect()
		self.client.subscribe(b"commands")
		self.client.subscribe(b"set")
		self.client.subscribe(b"start")
		self.stats = stats
		self.make_tea = make_tea
		self.abort = abort
		self.update_settings = update_settings
		self.loop = asyncio.get_event_loop()
		self.started = False

	def __exit__(self, exc_type, exc_value, traceback):
		self.client.loop_stop()
		self.client.disconnect()

	def begin(self):
		self.loop.create_task(self.process_msgs())
		self.loop.run_forever()

	def push_notification(self, data):
		"""
		Publish a push notification to connected devices with the state of the teapot
		:param data: string->string Python map of things to send
		"""
		self.client.publish(b"push", json.dumps(data).encode())

	async def process_msgs(self):
		while True:
			self.client.check_msg()
			await asyncio.sleep(2)

	def callback(self, topic, msg):
		if topic == b"commands":
			if msg == b"abort":
				if not self.started:
					return
				self.abort()
				self.started = False
			elif msg == b"stats":
				self.push_notification(self.stats())

		elif topic == b"set":
			settings = json.loads(msg.decode())
			self.update_settings(settings)

		elif topic == b"start":
			settings = json.loads(msg.decode())
			self.update_settings(settings)
			if not self.started:
				self.started = True
				self.loop.create_task(self.__manage_tea())

	async def __manage_tea(self):
		await self.make_tea()
		self.started = False

	def test(self, topic='Debug', message='Hello'):
		self.client.publish(topic.encode(), message.encode())
