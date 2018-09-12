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
	self.pub = rospy.Publisher('/arm', String) 
	# Define a and b(a is the x-height and b is the y-height)
	self.a = Float64()
	self.b = Float64()
	self.x = Float64()
	self.y = Float64()
	self.rx = Float64()
	self.rz = Float64()
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
	self.l1 = 0.17#0.161
	self.l3 = 0.1043
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
	def callback_nav2 (data_nav):
	    
	    if data_nav == "place":
	        rospy.loginfo( "I heard that the robot has reached point B")
	        self.armsub = 1
	    else:
	        self.armsub = 0
	# adding program above
	rospy.Subscriber("image_pos", pos, callback_pos)
	rospy.loginfo("Subscribe to topic pos.....")
	rospy.sleep(2)
        #adding program
	rospy.Subscriber("nav_chatter", Float64, callback_nav)
	rospy.loginfo("Subscribe to topic nav_chatter.....")
	rospy.sleep(2)
	######################
	rospy.Subscriber("/nav", String, callback_nav2)
	rospy.loginfo("Subscribe to topic image2arm.....")
	rospy.sleep(2)
	
	while not rospy.is_shutdown():
	    #rospy.loginfo("Test ......")
	    
	    # Define five initial poses 
		self.posi1 = Float64()
		self.posi2 = Float64()
		self.posi3 = Float64()
		self.posi4 = Float64()
		self.posi5 = Float64()
		# Define five poses
		self.pos1 = Float64()
		self.pos2 = Float64()
		self.pos3 = Float64()
		self.pos4 = Float64()
		self.pos5 = Float64()
		# Initial gesture of robot arm
		self.pos1 = 0#1.57#4.14
		self.pos2 = -1.4
		self.pos3 = 2.4
		self.pos4 = 0
		self.pos5 = -0.7
		self.joint1.publish(self.pos1)
		rospy.sleep(2)
		self.joint2.publish(self.pos2)
		rospy.sleep(2)
		self.joint3.publish(self.pos3)
		rospy.sleep(2)
		self.joint4.publish(self.pos4)
		rospy.sleep(2)
		self.joint5.publish(self.pos5)
		rospy.sleep(2)
		rospy.loginfo("Connecting to turtlebot arm....")
		if self.grasp == 1:
			self.a = self.x #used correct data before
			self.b = self.y 
			while self.b < 0:
			    rospy.loginfo("This coordinate is out of my location......")

			rospy.loginfo("The coordinate x we used to catch is ")
			print self.rx
			rospy.loginfo("The coordinate z we used to catch is ")
			print self.rz
			rospy.loginfo("X coordinate is ....") #print x coordinate
			print self.a
			rospy.loginfo("Y coordinate is ....") #print y coordinate
			print self.b
			# Make the diandong tuigan up to z coordinate
			#self.ddtg.publish(self.up)
			#rospy.sleep(1)
			#self.ddtg.publish(self.stop)
			       
			# gesture 1 the length of the arm is 33cm the longth between the second motor and the turtlebot is 5 cm 
			self.pos1 = self.posi1
			self.pos2 = self.posi2
			self.pos3 = self.posi3
			self.pos5 = self.posi5
			self.pos4 = -0.57
			self.joint2.publish(self.pos2)
			self.joint3.publish(self.pos3)
			self.joint4.publish(self.pos4)
			self.joint5.publish(self.pos5)
			rospy.sleep(4)
			self.joint1.publish(self.pos1)
			rospy.sleep(4)
			rospy.loginfo("Initial gesture ....")
	
			# calculate new joint angles
			self.l2 = math.hypot(self.a,self.b) #calculate l2
			self.theta1 = math.atan2(self.a,self.b)+0.1744+1.23 #To calculate the angle of rotation of joint one change a and b, add a diverge 0.1744
			rospy.loginfo("The rotation angle of joint one.....")
			print self.theta1
			self.tmp1 = self.l2 - self.l1
			self.tmp2 = self.tmp1/self.l3
			self.theta2 = math.asin(self.tmp2) # To calculate the angle of rotation of joint three and joint four
			rospy.loginfo("The rotation angle of joint three and four.....")
			print self.theta2
			self.posi21 = self.posi1 - self.theta1  
			self.posi23 = self.posi3 - self.theta2
			self.posi24 = self.posi4 + self.theta2
			self.posi25 = 0.5
			self.pos1 = self.posi21
			self.pos3 = self.posi23
			self.pos4 = self.posi24
			self.pos5 = self.posi25
			rospy.loginfo("Calculate new joint angles ......")
			# Rotate joint one to get the direction
			self.joint1.publish(self.pos1)
			rospy.sleep(4)
			# Stretched the arm
			self.joint2.publish(self.pos2)
			self.joint3.publish(self.pos3)
			self.joint4.publish(self.pos4)
			rospy.sleep(4)
			# Catch the goods
			self.joint5.publish(self.pos5)
			rospy.sleep(4)
			rospy.loginfo("Catch the goods ......")
			# Lift up the goods
			self.pos3 = self.posi3
			self.pos4 = self.posi4
			self.joint1.publish(self.pos1)
			self.joint2.publish(self.pos2)
			self.joint3.publish(self.pos3)
			self.joint4.publish(self.pos4)
			self.joint5.publish(self.pos5)
			rospy.loginfo("Lift up the goods for 5 seconds ......")
			rospy.sleep(5) #15 before
			self.image = "go"
			self.pub.publish(self.image)
			rospy.loginfo("I have grasped the item and please go to point B to place the item")
			if self.armsub == 1:
			    rospy.loginfo("Ready for releasing the goods")
			    # Release the goods
			    self.pos3 = self.posi23
			    self.pos4 = self.posi24
			    self.pos5 = self.posi5
			    self.joint1.publish(self.pos1)
			    rospy.sleep(4)
			    self.joint2.publish(self.pos2)
			    self.joint3.publish(self.pos3)
			    self.joint4.publish(self.pos4)
			    rospy.sleep(4)
			    self.joint5.publish(self.pos5)
			    rospy.loginfo("Release the goods ......")
			    rospy.sleep(4)
			    self.armsub = 0
			self.x = 10
			self.z = 10

    def cleanup(self):
        rospy.loginfo("Shutting down turtlebot arm....")

if __name__=="__main__":

    rospy.init_node('turtlebot_arm')
    try:
        Loop()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
