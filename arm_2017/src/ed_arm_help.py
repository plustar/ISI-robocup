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
	#self.ddtg = rospy.Publisher('toggle_msg',Float64)
	##############33
	self.grasped_pub = rospy.Publisher('/arm_grasped', String) 
	self.released_pub = rospy.Publisher('/arm_released', String)

	# the variable for diandong tuigan
	self.grasp = -1
	# adding program
	self.armsub = -1

	def callback_nav (data_nav):
		if data_nav.data.find('release') > -1:
			rospy.loginfo( "I heard that the robot has reached point B")
			self.armsub = 1
	def followStopCallback(data_stop):
		if data_stop.data.find('follow_stop') > -1:
			rospy.loginfo( "I heard that the robot has reached point A")
			self.grasp = 1
	# adding program above

	rospy.Subscriber("ifFollowme", String, followStopCallback)
	rospy.Subscriber("nav2image", String, callback_nav)
	rospy.loginfo("Subscribe to topic nav_chatter.....")
	rospy.sleep(2)

	# Define five poses
	self.pos1 = Float64()
	self.pos2 = Float64()
	self.pos3 = Float64()
	self.pos4 = Float64()
	self.pos5 = Float64()
	# Initial gesture of robot arm
	self.pos1 = 1.4#1.57#4.14
	self.pos2 = 1.57
	self.pos3 = -1.57
	self.pos4 = 0.6
	self.pos5 = -0.5
	
	self.joint5.publish(self.pos5)
	rospy.sleep(1)
	self.joint4.publish(self.pos4)
	rospy.sleep(1)
	self.joint3.publish(self.pos3)
	rospy.sleep(1)
	#self.joint2.publish(0.55)
	#rospy.sleep(1)
	self.joint1.publish(self.pos1)
	rospy.sleep(1)
	self.joint2.publish(self.pos2)
	rospy.sleep(1)

	rospy.loginfo("Connecting to turtlebot arm....")
	
	while not rospy.is_shutdown():
	    #rospy.loginfo("Test ......")
		
		if self.grasp == 1 and self.armsub == -1:
			# Rotate joint one to get the direction
			
			self.joint2.publish(1)
			rospy.sleep(1)
			self.joint1.publish(0)
			rospy.sleep(1)
			# Stretched the arm
			self.joint5.publish(0.6)
			rospy.sleep(2)	
			self.joint3.publish(-1.0)
			rospy.sleep(2)
			self.joint4.publish(-0.2)
			rospy.sleep(10)
			self.joint5.publish(-0.3)
			rospy.sleep(2)
			self.joint2.publish(2.0)	
			self.joint3.publish(-2.0)
			rospy.sleep(2)
			
			#self.joint3.publish(0.3)
			
			rospy.loginfo("Lift up the goods for 5 seconds ......")
			self.ifgrasped = "grasped"
			self.grasped_pub.publish(self.ifgrasped)
			rospy.loginfo("I have grasped the item and please go to point B to place the item")
			self.grasp = 0
		if self.armsub == 1 and self.grasp ==0:
			rospy.loginfo("Ready for releasing the goods")
			# Release the goods
			self.pos1 = 0
			self.pos2 = 1.4
			self.pos3 = 1.2
			self.pos4 = 1.2
			self.pos5 = 0.6
			self.joint1.publish(self.pos1)
			rospy.sleep(1)
			self.joint2.publish(self.pos2)
			self.joint3.publish(self.pos3)
			self.joint4.publish(self.pos4)
			rospy.sleep(1)
			self.joint5.publish(self.pos5)
			rospy.loginfo("Release the goods ......")
			rospy.sleep(3)
			self.armsub = 0
			self.grasp = -1
			self.ifreleased = "released"
			self.released_pub.publish(self.ifreleased)
			#reset the arm
			self.pos1 = 1.4#1.57#4.14
			self.pos2 = 1.57
			self.pos3 = -1.57
			self.pos4 = 0.6
			self.pos5 = -0.5
			
			self.joint5.publish(self.pos5)
			rospy.sleep(1)
			self.joint4.publish(self.pos4)
			rospy.sleep(1)
			self.joint3.publish(self.pos3)
			rospy.sleep(1)
			#self.joint2.publish(0.55)
			#rospy.sleep(1)
			self.joint1.publish(self.pos1)
			rospy.sleep(1)
			self.joint2.publish(self.pos2)
			rospy.sleep(1)

    def cleanup(self):
        rospy.loginfo("Shutting down turtlebot arm....")

if __name__=="__main__":

    rospy.init_node('turtlebot_arm')
    try:
        Loop()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

