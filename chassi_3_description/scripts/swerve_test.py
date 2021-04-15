#!/usr/bin/env python

import roslib; roslib.load_manifest('swerve')
import rospy
import tf.transformations
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
import math
from math import sqrt, fabs

pi = math.pi

def callback(msg):
    rospy.loginfo("Received a /cmd_vel message!")
    rospy.loginfo("Linear Components: [%f, %f, %f]"%(msg.linear.x, msg.linear.y, msg.linear.z))
    rospy.loginfo("Angular Components: [%f, %f, %f]"%(msg.angular.x, msg.angular.y, msg.angular.z))

    # Do velocity processing here:
    # Use the kinematics of your robot to map linear and angular velocities into motor commands
    y = msg.linear.x
    x = -(msg.linear.y)
    w = msg.angular.z
    
    L = 0.476
    W = 0.476
    R = (math.sqrt((L**2)+(W**2)))/2

    A = x + w*(L/2)
    B = x - w*(L/2)
    C = y + w*(W/2)
    D = y - w*(W/2)

    wm1 = math.sqrt((B**2)+(C**2))
    wm2 = math.sqrt((B**2)+(D**2))
    wm3 = math.sqrt((A**2)+(D**2))
    wm4 = math.sqrt((A**2)+(C**2))
    
    wp1 = math.atan2(B,C)
    wp2 = math.atan2(B,D)
    wp3 = math.atan2(A,D)
    wp4 = math.atan2(A,C)


    mx = max([wm1,wm2,wm3,wm4])
    if mx > 1:
        wm1/=mx
        wm2/=mx
        wm3/=mx
        wm4/=mx
    

    pubm1.publish(wm1)
    pubm2.publish(wm2)
    pubm3.publish(wm3)
    pubm4.publish(wm4)

    pubp1.publish(wp1)
    pubp2.publish(wp2)
    pubp3.publish(wp3)
    pubp4.publish(wp4)

def listener():
    rospy.init_node('cmd_vel_listener')
    rospy.Subscriber("/cmd_vel", Twist, callback)
    rospy.spin()

def mapFloat(x1, out_min, out_max):
    return min([out_min + ((x1-x_min)/(x_max-x_min))*(out_max-out_min), out_max])

if __name__ == '__main__':
    pubm1 = rospy.Publisher('/motor1_position_controller/command', Float64, queue_size=1)
    pubm2 = rospy.Publisher('/motor2_position_controller/command', Float64, queue_size=1)
    pubm3 = rospy.Publisher('/motor3_position_controller/command', Float64, queue_size=1)
    pubm4 = rospy.Publisher('/motor4_position_controller/command', Float64, queue_size=1)

    pubp1 = rospy.Publisher('/pivot1_position_controller/command', Float64, queue_size=1)
    pubp2 = rospy.Publisher('/pivot2_position_controller/command', Float64, queue_size=1)
    pubp3 = rospy.Publisher('/pivot3_position_controller/command', Float64, queue_size=1)
    pubp4 = rospy.Publisher('/pivot4_position_controller/command', Float64, queue_size=1)
    listener()