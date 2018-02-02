from machine import PWM


class Servo:
	__pwm = None

	def __init__(self, motor_pin, start_position=0.5):
		self.__pwm = PWM(motor_pin, freq=50)
		self.set_position(start_position)

	def set_position(self, p):
		pos = max(0.0, min(1.0, p))
		duty = int(30.0 + pos * 90.0)
		self.__pwm.duty(duty)
