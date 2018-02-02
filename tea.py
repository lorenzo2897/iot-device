
import uasyncio as asyncio


def stats():
	print("stats requested")
	data = {
		"name": "John Smith"
	}
	return data


async def make_tea():
	while True:
		print("started")
		await asyncio.sleep(5)


def abort():
	print("aborted")


def update_settings(settings):
	print(settings)
