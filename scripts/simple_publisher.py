#!/usr/bin/env python
# Publishes a random number between 0 and 10.
from random import random
import rospy
import random
from std_msgs.msg import Float32

def talker():
    pub = rospy.Publisher('my_random_float', Float32, queue_size=10)
    rospy.init_node('simple_publisher', anonymous=True)
    rate = rospy.Rate(20) # 20hz
    while not rospy.is_shutdown():
        # hello_str = "hello world %s" % rospy.get_time()
        random_number = 10*random.random()
        rospy.loginfo(random_number)
        pub.publish(random_number)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass