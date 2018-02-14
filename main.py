from mqtt.MQTTembedded import IotClient
import network
import utime

# tests
from drivers.infrared import Infrared
from drivers.rgb import RGB

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
	tea_maker = Tea()
	status_led.on()  # active-low
	activate_network()
	client = IotClient("silvestri.io", tea_maker.stats, tea_maker.make_tea, tea_maker.abort, tea_maker.update_settings)
	tea_maker.send_push = client.push_notification
	client.begin()


def setup():
	global servo, rgb, ir_b, ir_t
	ir_b = Infrared(sda=Pin(4), scl=Pin(5), addr=0x41, samplerate=4)
	ir_t = Infrared(sda=Pin(4), scl=Pin(5), addr=0x45, samplerate=4)
	rgb = RGB(sda=Pin(4), scl=Pin(5), led=Pin(2, Pin.OUT))
	servo = Servo(Pin(12), 0.4)

	rgb.begin()
	rgb.set_led(1)


def test():
	global servo, rgb, ir_b, ir_t

	t = 0
	while True:
		temp_b = ir_b.read_temperature()
		temp_t = ir_t.read_temperature()
		col = rgb.read_color()[0]
		print(t, temp_b, temp_t, col, sep="\t")
		utime.sleep(1)
		t += 1


status_led.on()  # active-low
if __name__ == '__main__':
	pass
	# setup()
	# main()
