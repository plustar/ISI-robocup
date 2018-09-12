#!/usr/bin/env python

# new calculating algorithm
import rospy
import math
from std_msgs.msg import String
from std_msgs.msg import Float64

class Loop:
    def __init__(self):
	rospy.on_shutdown(self.cleanup)

        init_pose = (1.57,2.0,-2.0,1.7,-0.5)
        #init_pose = (0,1.57,0.7,0.7,0.5)
        hold_pose = (0,1,-2,1,-0.3)

        set_pose = (0,1.57,0.7,0.7,0.5)
        
	self.joint1 = rospy.Publisher('/arm_shoulder_pan_joint/command',Float64)
	self.joint2 = rospy.Publisher('/arm_shoulder_lift_joint/command',Float64)
	self.joint3 = rospy.Publisher('/arm_elbow_flex_joint/command',Float64)
	self.joint4 = rospy.Publisher('/arm_wrist_flex_joint/command',Float64)
	self.joint5 = rospy.Publisher('/gripper_joint/command',Float64)

	#mark for different poses
	self.mark = 0

	self.a2 = 0.105
	self.a3 = 0.105
	self.a4 = 0.09
	self.arm_length = 0.29
	
	self.grasp = -1
	self.armsub = -1
	def callback_nav(data_nav):
		if data_nav.data.find('release') > -1:
		    rospy.loginfo( "I heard that the robot has reached point B")
			self.armsub = 1
	def followStopCallback(data_stop):
		if data_stop.data.find('follow_stop') > -1:
			rospy.loginfo( "I heard that the robot has reached point A")
			self.grasp = 1
	# adding program above
	rospy.Subscriber("nav2arm",String, callback_nav)
	rospy.Subscriber(¨ifFollowme¨,String,follwStopCallback)
	rospy.loginfo("Subscribe to topic carry .....")
	rospy.sleep(2)
	######################
	# Define five poses
	
	self.joint1.publish(init_pose[0])
	rospy.sleep(2)
	self.joint2.publish(init_pose[1])
	rospy.sleep(2)
	self.joint3.publish(init_pose[2])
	rospy.sleep(2)
	self.joint4.publish(init_pose[3])
	rospy.sleep(2)
	self.joint5.publish(init_pose[4])
	rospy.sleep(2)

	rospy.loginfo("Connecting to turtlebot arm....")
	
	while not rospy.is_shutdown():
            
	    #rospy.loginfo("Test ......")
		
		if self.grasp == 1 and self.armsub == -1:

			# Rotate joint one to get the direction
			self.joint1.publish(hold_pose[0])
			rospy.sleep(2)
			self.joint2.publish(hold_pose[1])
			rospy.sleep(2)
			self.joint3.publish(hold_pose[2])
			rospy.sleep(2)
			self.joint4.publish(hold_pose[3])
			rospy.sleep(2)
			self.joint5.publish(hold_pose[4])
			rospy.sleep(2)
			self.grasp = 0
			
		if self.grasp == 0 and self.armsub == 1:
			    
			self.joint5.publish(init_pose[4])
			rospy.sleep(2)
			self.joint4.publish(init_pose[3])
			rospy.sleep(2)
			self.joint3.publish(init_pose[2])
			rospy.sleep(2)
			self.joint2.publish(init_pose[1])
			rospy.sleep(2)
			self.joint1.publish(init_pose[0])
			rospy.sleep(2)
			self.joint2.publish(set_pose[1])
			rospy.sleep(2)
			self.joint4.publish(set_pose[3])
			rospy.sleep(2)
			self.joint3.publish(set_pose[2])
			rospy.sleep(2)
			self.joint5.publish(set_pose[4])
			rospy.sleep(2)
			self.grasp = -1
			self.armsub ==  -1
	def cleanup(self):
		rospy.loginfo("Shutting down turtlebot arm....")

if __name__=="__main__":

	rospy.init_node('turtlebot_arm')
	try:
		Loop()
		rospy.spin()
	except rospy.ROSInterruptException:
		pass

