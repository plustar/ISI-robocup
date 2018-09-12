#!/usr/bin/env python

# new calculating algorithm
import rospy
import math
from std_msgs.msg import String
from std_msgs.msg import Float64
from arm_2017.msg import pos

class Loop:
	def __init__(self):
		rospy.on_shutdown(self.cleanup)
		# publish command message to joints/servos of arm
		self.joint1 = rospy.Publisher('/arm_shoulder_pan_joint/command',Float64)
		self.joint2 = rospy.Publisher('/arm_shoulder_lift_joint/command',Float64)
		self.joint3 = rospy.Publisher('/arm_elbow_flex_joint/command',Float64)
		self.joint4 = rospy.Publisher('/arm_wrist_flex_joint/command',Float64)
		self.joint5 = rospy.Publisher('/gripper_joint/command',Float64)

		# Define five poses
		self.pos1 = Float64()
		self.pos2 = Float64()
		self.pos3 = Float64()
		self.pos4 = Float64()
		self.pos5 = Float64()

	# Initial gesture of robot arm
		self.pos1 = 0#1.57#4.14
		self.pos2 = -1.1
		self.pos3 = 2.2
		self.pos4 = 1
		self.pos5 = -0.4
		
		self.joint1.publish(self.pos1)
		rospy.sleep(1)
		self.joint5.publish(self.pos5)
		rospy.sleep(1)
		self.joint4.publish(self.pos4)
		rospy.sleep(1)
		self.joint3.publish(2.2)
		rospy.sleep(1)
		self.joint2.publish(self.pos2)
		rospy.sleep(5)

		rospy.loginfo("Connecting to turtlebot arm....")
		self.pos1 = 0#1.57#4.14
		self.pos2 = 1
		self.pos3 =-1
		self.pos4 = 0
		self.pos5 = -0.2
		self.joint5.publish(self.pos5)
		rospy.sleep(1)
		self.joint1.publish(self.pos1)
		self.joint2.publish(self.pos2)
		self.joint3.publish(self.pos3)
		self.joint4.publish(self.pos4)
		rospy.loginfo("Lift up the goods for 5 seconds ......")
		rospy.sleep(5) #15 before
		
		self.pos1 = 0
		self.pos2 = 1
		self.pos3 = -0.1
		self.pos4 = 0.5
		self.pos5 = 0.6
		self.joint1.publish(self.pos1)
		rospy.sleep(1)
		self.joint2.publish(self.pos2)
		self.joint3.publish(self.pos3)
		self.joint4.publish(self.pos4)
		rospy.sleep(1)
		self.joint5.publish(self.pos5)
		rospy.loginfo("Release the goods ......")
		rospy.sleep(5)

		# Initial gesture of robot arm
		self.pos1 = 0#1.57#4.14
		self.pos2 = -1.1
		self.pos3 = 2.2
		self.pos4 = 1
		self.pos5 = -0.4
		
		self.joint1.publish(self.pos1)
		rospy.sleep(1)
		self.joint2.publish(0.9)
		self.joint3.publish(0.8)
		self.joint4.publish(self.pos4)
		rospy.sleep(1)
		self.joint2.publish(self.pos2)
		rospy.sleep(1)
		self.joint3.publish(self.pos3)
		rospy.sleep(1)
		self.joint5.publish(self.pos5)
		rospy.sleep(1)
		rospy.loginfo("reset turtlebot arm....")
	def cleanup(self):
		rospy.loginfo("Shutting down turtlebot arm....")

if __name__=="__main__":

	rospy.init_node('turtlebot_arm')
	try:
		Loop()
		rospy.spin()
	except rospy.ROSInterruptException:
		pass

