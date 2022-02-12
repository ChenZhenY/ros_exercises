#!/usr/bin/env python
# Publishes a random number between 0 and 10.
from cmath import pi
import rospy
import numpy as np
from sensor_msgs.msg import LaserScan

def talker():
    scan_rate = rospy.get_param('scan_rate', 20)
    scan_name = rospy.get_param('scan_name', 'fake_scan')

    pub = rospy.Publisher(scan_name, LaserScan, queue_size=10)
    rospy.init_node('fake_scan_publisher', anonymous=True)
    rate = rospy.Rate(scan_rate) # 20hz
    now = rospy.Time.now() #get_time()
    last = rospy.Time.now()

    angle_min = rospy.get_param('angle_min', -2*pi/3.0)
    angle_max = rospy.get_param('angle_max', 2*pi/3.0)
    range_min = rospy.get_param('range_min', 1.0)
    range_max = rospy.get_param('aaa/range_max', 10.0) 
    angle_increment = rospy.get_param('~angle_increment', pi/300.0)
    # private namespace ~, need to specify param in launch file accordingly ~

    rospy.loginfo(range_max)

    scan_msg = LaserScan()
    scan_msg.angle_min = angle_min
    scan_msg.angle_max = angle_max
    scan_msg.angle_increment = angle_increment
    scan_msg.range_min = range_min
    scan_msg.range_max = range_max
    # scan_msg.time_increment = 0.1 # unimportant
    # scan_msg.intensities = 1      # unimportant

    while not rospy.is_shutdown():
        now = rospy.Time.now()    # now might be better? get_time()
        # scan_msg.scan_time = now - last
        scan_msg.header.stamp = now
        scan_msg.header.frame_id = 'base_link'
        length = int(np.rint((angle_max-angle_min)/angle_increment) + 1)
        ranges = np.random.rand(length)*(range_max-range_min)+range_min  # 1 dimension array! 
        scan_msg.ranges = ranges.tolist()

        # rospy.loginfo(scan_msg)
        pub.publish(scan_msg)
        last = now
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass