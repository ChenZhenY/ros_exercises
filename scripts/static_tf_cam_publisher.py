#!/usr/bin/env python
import rospy

# to get commandline arguments
import sys

# because of transformations
import tf

import tf2_ros
import geometry_msgs.msg

# why still no transformation from left_cam to base_link?
if __name__ == '__main__':


    rospy.init_node('my_static_tf2_broadcaster')

    broadcaster = tf2_ros.StaticTransformBroadcaster()
    static_transformStamped = geometry_msgs.msg.TransformStamped()

    static_transformStamped.header.stamp = rospy.Time.now()
    static_transformStamped.header.frame_id = "base_link_gt"
    static_transformStamped.child_frame_id = "left_cam"

    static_transformStamped.transform.translation.x = -0.05
    static_transformStamped.transform.translation.y = 0
    static_transformStamped.transform.translation.z = 0

    quat = tf.transformations.quaternion_from_euler(0,0,0)
    static_transformStamped.transform.rotation.x = quat[0]
    static_transformStamped.transform.rotation.y = quat[1]
    static_transformStamped.transform.rotation.z = quat[2]
    static_transformStamped.transform.rotation.w = quat[3]

    # broadcaster.sendTransform(static_transformStamped)


    # broadcaster1 = tf2_ros.StaticTransformBroadcaster()
    static_transformStamped1 = geometry_msgs.msg.TransformStamped()

    static_transformStamped1.header.stamp = rospy.Time.now()
    static_transformStamped1.header.frame_id = "left_cam"
    static_transformStamped1.child_frame_id = "right_cam"

    static_transformStamped1.transform.translation.x = 0.1
    static_transformStamped1.transform.translation.y = 0
    static_transformStamped1.transform.translation.z = 0

    quat = tf.transformations.quaternion_from_euler(0,0,0)
    static_transformStamped1.transform.rotation.x = quat[0]
    static_transformStamped1.transform.rotation.y = quat[1]
    static_transformStamped1.transform.rotation.z = quat[2]
    static_transformStamped1.transform.rotation.w = quat[3]
    # TODO: the right way to send two transform at a time
    broadcaster.sendTransform([static_transformStamped1, static_transformStamped])

    rospy.spin()