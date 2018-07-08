import paho.mqtt.client as mqtt
import socket
import base64

DEFAULT_BROKER_HOSTNAME = "localhost"
TOPIC_MOVE_NAME = "im/command/head/facetrackmove"
TOPIC_START_NAME = "im/command/head/facetrackstart"

class CommandRobot(object):
    """
        Launch command to the broker
    """

    def __init__(self, hostname = DEFAULT_BROKER_HOSTNAME):
        print ("trying to connect with {}".format(hostname))
        self.mqtt_client = mqtt.Client(client_id="camera_"+socket.gethostname())
        self.mqtt_client.connect(hostname, 1883, 60)

    def move(self, position):
        """
            Method to publish a move event to the broker
        """

        print ("move at {}".format(position))
        self.mqtt_client.publish(TOPIC_MOVE_NAME, "{{\"origin\":\"camera\",\"absPosition\":{0}}}".format(position))

    def post_photo(self, img):
        """
            Method to publish a photo to the broker
        """

        print("take photo !!!")
        b64img=base64.b64encode(img)
        #b64img=b64img.decode("utf-8")
        print("photo b64: {}".format(b64img)) 
        self.mqtt_client.publish(TOPIC_START_NAME, "{{\"origin\":\"camera\",\"face\":\"{0}\"}}".format(b64img))
