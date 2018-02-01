from machine import Pin
from sensors.rgb import RGB
from sensors.temperature import Temperature
import utime

rgb = RGB(sda=Pin(4), scl=Pin(5), led=Pin(16, Pin.OUT))
temp = Temperature(sda=Pin(4), scl=Pin(5))


def main():
	rgb.begin(50, 4)

	while 1:
		# print(rgb.read_color())  # end='         \r'

		utime.sleep(1)


if __name__ == '__main__':
	# main()
	pass
