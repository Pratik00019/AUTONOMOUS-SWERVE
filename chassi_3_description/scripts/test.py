#!/usr/bin/env python

import rospy
from std_msgs.msg import Int8

def talker():
	pub=rospy.Publisher("chatter",Int8,queue_size=10)
	rospy.init_node("talker",anonymous=True)
	rate=rospy.Rate(1)
	while not rospy.is_shutdown():
		hell=5
		rospy.loginfo(hell)
		pub.publish(hell)
		rate.sleep()

if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass