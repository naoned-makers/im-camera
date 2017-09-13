import paho.mqtt.publish as publish


def stop_command():
    print("stop move")

def start_command(position):
    #todo : start move
    print "start moving at {}".format(position)
    publish.single("im/command/head/facetrackmove", "{{\"origin\":\"camera\",\"absPosition\":{0}}}".format(position), hostname="localhost")

def move(position):
    print "move at {}".format(position)
    publish.single("im/command/head/facetrackmove", "{{\"origin\":\"camera\",\"absPosition\":{0}}}".format(position), hostname="localhost")