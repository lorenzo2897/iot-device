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
		self.stats = stats
		self.make_tea = make_tea
		self.abort = abort
		self.update_settings = update_settings
		self.loop = asyncio.get_event_loop()

	def __exit__(self, exc_type, exc_value, traceback):
		self.client.loop_stop()
		self.client.disconnect()

	def begin(self):
		self.loop.create_task(self.process_msgs())
		self.loop.run_forever()

	def push_notification(self, content):
		self.client.publish(b"push", content.encode())

	async def process_msgs(self):
		while True:
			self.client.check_msg()
			await asyncio.sleep(5)

	def callback(self, topic, msg):
		if topic == b"commands":
			if msg == b"make_tea":
				self.loop.create_task(self.make_tea())
			elif msg == b"abort":
				self.abort()
			elif msg == b"stats":
				self.client.publish(b"stats", json.dumps(self.stats()).encode())
		elif topic == b"set":
			settings = json.loads(msg.decode())
			self.update_settings(settings)

	def test(self, topic='Debug', message='Hello'):
		self.client.publish(topic.encode(), message.encode())
