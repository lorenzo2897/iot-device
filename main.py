from mqtt.MQTTembedded import IotClient
import uasyncio as asyncio
import network

#Sample functions, use same structure
import json
def stats():
	data = '{"name": "John Smith", "hometown": {"name": "New York", "id": 123}}'
	x = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
	return x

async def make_tea():
	while True:
		print("started")
		await asyncio.sleep(5)

def abort():
	print("aborted")

def update_settings(settings):
	print(json.dumps(settings))


#connect to hotspot
def activate_network():
	ap_if = network.WLAN(network.AP_IF)
	ap_if.active(False)

	sta_if = network.WLAN(network.STA_IF)
	sta_if.active(True)
	sta_if.connect('OnePlus 3', 'a10101010a')

def main():
	client = IotClient("silvestri.io", stats, make_tea, abort, update_settings)
	client.begin()

#if __name__ == '__main__':
#	main()
