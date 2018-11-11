import paho.mqtt.client as mqtt
import socket
import base64

TOPIC_MOVE_NAME = "im/command/head/facetrackmove"
TOPIC_START_NAME = "im/command/head/facetrackstart"

class CommandRobot(object):
    """
        Launch command to the broker
    """

    def __init__(self, hostname):
        self.mqtt_client = None

        if hostname is not None:
            print ("trying to connect with {}".format(hostname))
            self.mqtt_client = mqtt.Client(client_id="camera_"+socket.gethostname())
            self.mqtt_client.connect(hostname, 1883, 60)

    def move(self, position):
        """
            Method to publish a move event to the broker
        """

        if self.mqtt_client is not None:
            print ("move at {}".format(position))
            self.mqtt_client.publish(TOPIC_MOVE_NAME, "{{\"origin\":\"camera\",\"absPosition\":{0}}}".format(position))

    def post_photo(self, img):
        """
            Method to publish a photo to the broker
        """

        if self.mqtt_client is not None:

            print("take photo !!!")
            b64img=base64.b64encode(img)
            str_encoded=str(b64img,'utf-8')

            with open("test_encoded.txt", "w") as text_file:
                text_file.write(str_encoded)
            
            self.mqtt_client.publish(TOPIC_START_NAME, "{{\"origin\":\"camera\",\"face\":\"{0}\"}}".format(str_encoded))
