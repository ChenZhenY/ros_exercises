#!/usr/bin/env python
# Publishes a random number between 0 and 10.
from random import random
import rospy
import random
from ros_exercises.msg import OpenSpace
from std_msgs.msg import Float32
from sensor_msgs.msg import LaserScan

class OpenSpacePub ():
    def __init__(self):
        self.value = 0
        self.space_msg = OpenSpace()
        self.pub_topic = rospy.get_param('open_pub', '/open_space')
        self.sub_topic = rospy.get_param('open_sub', '/fake_scan')
        rospy.init_node('open_space_publisher', anonymous=True)
        # self.pub_dist = rospy.Publisher('/open_space/distance',Float32,queue_size=10)
        # self.pub_angle = rospy.Publisher('/open_space/angle',Float32,queue_size=10)
        self.pub_space = rospy.Publisher(self.pub_topic,OpenSpace,queue_size=10)
        rospy.Subscriber(self.sub_topic, LaserScan, self.listener)

    def listener(self, msg):
        self.range = msg.ranges
        self.max_range = max(self.range)
        self.max_angle = self.range.index(self.max_range) # only get first occurence
        self.space_msg.angle = self.max_angle
        self.space_msg.distance = self.max_range
        self.pub_space.publish(self.space_msg)
        # self.pub_dist.publish(self.max_range)
        # self.pub_angle.publish(self.max_angle)
        # rospy.loginfo(self.max_angle)

    def spin(self):
        rate = rospy.Rate(20)
        rospy.spin()

if __name__ == '__main__':
    OpenSpace1 = OpenSpacePub()
    try:
        OpenSpace1.spin()
    except rospy.ROSInterruptException:
        pass