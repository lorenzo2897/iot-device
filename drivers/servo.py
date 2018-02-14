from machine import PWM
import utime

class Servo:
	__pwm = None
	__position = 0.5

	def __init__(self, motor_pin, start_position=0.5):
		self.__pwm = PWM(motor_pin, freq=50)
		self.set_position(start_position)

	def set_position(self, p):
		self.__position = max(0.0, min(1.0, p))
		duty = int(35.0 + self.__position * 80.0)
		self.__pwm.duty(duty)

	def get_position(self):
		return self.__position

	def sweep(self, p):
		target = max(0.0, min(1.0, p))
		current = self.__position
		step = (target - current) / 20
		for i in range(0, 20):
			self.set_position(current + step * i)
			utime.sleep_ms(100)

		self.set_position(target)
