from mqtt.MQTTembedded import IotClient
from machine import Pin
import network
import utime

from tea import *

status_led = Pin(0, Pin.OUT)


# connect to hotspot
def activate_network():
	ap_if = network.WLAN(network.AP_IF)
	ap_if.active(False)

	sta_if = network.WLAN(network.STA_IF)
	sta_if.active(True)
	sta_if.connect('compatriots', 'a10101010a')

	while not sta_if.isconnected():
		utime.sleep_ms(500)
		status_led.value(not status_led.value())

	status_led.off()  # active-low


def main():
	status_led.on()  # active-low
	activate_network()
	client = IotClient("silvestri.io", stats, make_tea, abort, update_settings)
	client.begin()


#if __name__ == '__main__':
#	main()
