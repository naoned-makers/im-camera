import paho.mqtt.publish as publish

DEFAULT_BROKER_HOSTNAME = "localhost"
TOPIC_MOVE_NAME = "im/command/head/facetrackmove"


class CommandRobot(object):
    """
        Launch command to the broker
    """

    def __init__(self, hostname = DEFAULT_BROKER_HOSTNAME, topic_name = TOPIC_MOVE_NAME):
        self.hostname = hostname
        self.topic_name = topic_name

    def move(self, position):
        """
            Method to publish a move event to the broker
        """

        print "move at {}".format(position)
        publish.single(self.topic_name, "{{\"origin\":\"camera\",\"absPosition\":{0}}}".format(position), hostname=self.hostname)