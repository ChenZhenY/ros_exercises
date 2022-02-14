#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32

def callback(data, pub):
    pub.publish(data.data)
    # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('simple_subscriber', anonymous=True)

    pub = rospy.Publisher('random_float_log', Float32, queue_size=10)
    rospy.Subscriber("my_random_float", Float32, callback, pub)
    
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()