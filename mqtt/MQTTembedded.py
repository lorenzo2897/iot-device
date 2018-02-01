from umqtt.simple import MQTTClient

class IotClient:
    #add stats function
    def __init__(self, ip, port, stats_callback):
        self.client = MQTTClient()
        self.client.connect(ip, port, 60)
        self.client.loop_start()

    def __exit__(self, exc_type, exc_value, traceback):
        self.client.loop_stop()
        self.client.disconnect()

	#content JSON string
    def push_notification(self, content):
    def callback(self, )
    def test(self, topic = 'Debug', message = 'Hello'):
        self.client.publish(topic, message)
    