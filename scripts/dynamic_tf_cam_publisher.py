#!/usr/bin/env python  
from cgi import print_environ_usage
from multiprocessing.connection import Listener
import roslib
import rospy
import numpy as np
import tf2_ros
import tf
import geometry_msgs.msg

# def handle_turtle_pose(msg, turtlename):
    
#     br.sendTransform((msg.x, msg.y, 0),
#                      tf.transformations.quaternion_from_euler(0, 0, msg.theta),
#                      rospy.Time.now(),
#                      turtlename,
#                      "world")

def get_transformation_matrix(trans, rot):
    trans_matrix = tf.transformations.quaternion_matrix(rot)
    trans_matrix[0:3, 3] = np.array(trans).T
    return trans_matrix

def calc_br_transforms(tr, br):
    # TODO: fix here
    trans = [tr.transform.translation.x, tr.transform.translation.z, tr.transform.translation.y]
    # trans = [tr.transform.translation.x, tr.transform.translation.y, tr.transform.translation.z]

    rot   = [tr.transform.rotation.x, tr.transform.rotation.y, tr.transform.rotation.z, tr.transform.rotation.w]
    
    trans_left = [trans[0]-0.05, trans[1], trans[2]]
    # print(trans_left)

    robot_trans_matrix = get_transformation_matrix(trans, rot)
    left2right_matrix  = get_transformation_matrix([0.1, 0, 0], [0,0,0,1])  # xyzw
    left_trans_matrix  = get_transformation_matrix(trans_left, rot)
    right_trans_matrix = np.dot(left2right_matrix, left_trans_matrix)

    rotq_right = tf.transformations.quaternion_from_matrix(right_trans_matrix)
    
    t = geometry_msgs.msg.TransformStamped()
    # left cam transfrom
    t.header.stamp = rospy.Time.now()
    t.header.frame_id = "world"
    t.child_frame_id = "left_cam"
    t.transform.translation.x = trans_left[0]
    t.transform.translation.y = trans_left[1]
    t.transform.translation.z = trans_left[2]
    # q = tf_conversions.transformations.quaternion_from_euler(0, 0, msg.theta)
    t.transform.rotation.x = rot[0]
    t.transform.rotation.y = rot[1]
    t.transform.rotation.z = rot[2]
    t.transform.rotation.w = rot[3]
    br.sendTransform(t)

    t.header.frame_id = "left_cam"
    t.child_frame_id = "right_cam"
    t.transform.translation.x = right_trans_matrix[0,2]
    t.transform.translation.y = right_trans_matrix[1,2]
    t.transform.translation.z = right_trans_matrix[2,2]
    # q = tf_conversions.transformations.quaternion_from_euler(0, 0, msg.theta)
    t.transform.rotation.x = rotq_right[0]
    t.transform.rotation.y = rotq_right[1]
    t.transform.rotation.z = rotq_right[2]
    t.transform.rotation.w = rotq_right[3]
    br.sendTransform(t)

if __name__ == '__main__':
    rospy.init_node('dynamic_tf_cam_publisher')
    rate = rospy.Rate(10)
    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)
    br = tf2_ros.TransformBroadcaster()
    
    while not rospy.is_shutdown():
        try:
            tr = tfBuffer.lookup_transform('base_link_gt', 'world', rospy.Time())
            # br.sendTransform(tr) # send back base_link transform
            calc_br_transforms(tr, br)
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            rospy.loginfo("can't get transform")
            rate.sleep()
            continue



