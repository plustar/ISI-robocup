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
		self.ddtg = rospy.Publisher('toggle_msg',Float64)
		##############33
		self.pub = rospy.Publisher('/armOK', String) 
		# Define a and b(a is the x-height and b is the y-height)
		self.a = Float64()
		self.b = Float64()
		self.x = Float64()
		self.y = Float64()
		self.rx = Float64()
		self.rz = Float64()
		self.finishdata = String()
		# adding program
		self.nav = Float64() #the number which is used to get the order from node goforward
		# Subscribe three topics to get the x, y, z coordinate
		self.x = 10
		self.y = 10
		self.z = 10
		# the variable for diandong tuigan
		self.grasp = 0
		# adding program
		self.nav = 0
		self.armsub = 0
		self.a2 = 0.105
		self.a3 = 0.105
		self.a4 = 0.09
		self.arm_length = 0.29
		self.finishdata = 'finish'
		
		def callback_pos (data_pos):
			rospy.loginfo(rospy.get_caller_id() + "I heard that coordinate is %s", data_pos)
			self.grasp = 1
			self.x = data_pos.x
			self.y = data_pos.y
			self.z = data_pos.z
			self.rx = self.x
		# adding program
		def callback_nav (data_nav):
			rospy.loginfo( "I heard that the robot has reached the place")
			self.nav = data_nav
			print self.nav
		def callback_sp (data_sp):
			rospy.loginfo("In the callback_sp")
			print data_sp
			if data_sp.data.find('finish') > -1:
				self.armsub = 1
				rospy.loginfo("I have heard that robot has reached point B")
			else:
				self.armsub = 0
				rospy.loginfo("no input from isfinish")
		# adding program above
		rospy.Subscriber("image_pos", pos, callback_pos)
		rospy.loginfo("Subscribe to topic pos.....")
		rospy.sleep(2)
		#adding program
		rospy.Subscriber("nav_chatter", Float64, callback_nav)
		rospy.loginfo("Subscribe to topic nav_chatter.....")
		rospy.sleep(2)
		######################
		rospy.Subscriber("isfinish", String, callback_sp)
		rospy.loginfo("Subscribe to topic image2arm.....")
		rospy.sleep(2)
		# Define five poses
		self.pos1 = Float64()
		self.pos2 = Float64()
		self.pos3 = Float64()
		self.pos4 = Float64()
		self.pos5 = Float64()

		rospy.loginfo("Connecting to turtlebot arm....")
		self.pos1 = 0
		self.pos2 = 0.7
		self.pos3 = -0.8
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
		rospy.sleep(10)
		# Initial gesture of robot arm
		self.pos1 = 0#1.57#4.14
		self.pos2 = -1.1
		self.pos3 = 2.1
		self.pos4 = 1
		self.pos5 = -0.4
	
		self.joint1.publish(self.pos1)
		rospy.sleep(2)
		self.joint5.publish(self.pos5)
		rospy.sleep(2)
		self.joint4.publish(self.pos4)
		rospy.sleep(2)
		self.joint3.publish(2.1)
		rospy.sleep(2)
		self.joint2.publish(self.pos2)
		rospy.sleep(2)
		self.joint3.publish(self.pos3)
		rospy.sleep(2)

	def cleanup(self):
		rospy.loginfo("Shutting down turtlebot arm....")

if __name__=="__main__":

	rospy.init_node('turtlebot_arm')
	try:
		Loop()
		rospy.spin()
	except rospy.ROSInterruptException:
		pass

