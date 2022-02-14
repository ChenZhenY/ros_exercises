#!/usr/bin/env python  
from cgi import print_environ_usage
from multiprocessing.connection import Listener
import roslib
import rospy
import numpy as np
import tf2_ros
import tf
import geometry_msgs.msg

def send_new_transforms(tr, br):
    trans = [tr.transform.translation.x, tr.transform.translation.y, tr.transform.translation.z]
    rot   = [tr.transform.rotation.x, tr.transform.rotation.y, tr.transform.rotation.z, tr.transform.rotation.w]
    
    t = geometry_msgs.msg.TransformStamped()
    # left cam transfrom
    t.header.stamp = rospy.Time.now()
    t.header.frame_id = "world"
    t.child_frame_id = "base_link_gt2"
    t.transform.translation.x = trans[0] + 0.05
    t.transform.translation.y = trans[1]
    t.transform.translation.z = trans[2]
    # q = tf_conversions.transformations.quaternion_from_euler(0, 0, msg.theta)
    t.transform.rotation.x = rot[0]
    t.transform.rotation.y = rot[1]
    t.transform.rotation.z = rot[2]
    t.transform.rotation.w = rot[3]
    
    # print(trans)
    br.sendTransform(t)


if __name__ == '__main__':
    rospy.init_node('base_link_tf_pub')
    rate = rospy.Rate(10)
    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)
    br = tf2_ros.TransformBroadcaster()
    
    while not rospy.is_shutdown():
        try:
            # tr = tfBuffer.lookup_transform('left_cam', 'world', rospy.Time())
            tr = tfBuffer.lookup_transform('world', 'left_cam', rospy.Time())
            # TODO: means transform from left_cam to world/
            send_new_transforms(tr, br)
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            rospy.loginfo("can't get transform")
            rate.sleep()
            continue