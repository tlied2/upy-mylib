from umqtt.simple import MQTTClient


def sub_callback(topic, msg):
    print(("MQTT Message: {} | {}".format(topic, msg)))


class MyMQTT(object):

    def __init__(self, config):
        self.config = config
        self.connected = False
        self.client = MQTTClient(
            self.config['clientname'],
            self.config['server'])
        self.connect()

    def connect(self):
        try:
            print(("Connecting to MQTT host: %s" % (self.config['server'])))
            self.client.connect(clean_session=False)
            self.connected = True
        except OSError:
            self.connected = False
            print("Unable to connect to MQTT")

    def sub(self, topic, callback=sub_callback):
        if not self.connected:
            self.connect()
        if self.connected:
            self.client.set_callback(callback)
            self.client.subscribe(topic)
        else:
            print(("MQTT not connected, not subscribing to %s" % (topic)))

    def pub(self, topic, data):
        if not self.connected:
            self.connect()
        if self.connected:
            try:
                print(("Publishing data to MQTT: %s" % data))
                self.client.publish(topic, data, retain=True, qos=1)
            except Exception as tmpex:
                self.connected = False
                print(("Error publishing to MQTT: %s" % tmpex))
                self.close()
        else:
            print(("MQTT not connected, not publishing %s:%s" % (topic, data)))

    def close(self):
        self.client.disconnect()

    def check(self):
        self.client.check_msg()
