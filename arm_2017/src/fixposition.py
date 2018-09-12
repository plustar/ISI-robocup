#!/usr/bin/env python

"""
    crane_arm.py - move crane arm according to predefined gestures

"""
"""
import rospy
from std_msgs.msg import Float64

class Loop:
    def __init__(self):
        rospy.on_shutdown(self.cleanup)

	# publish command message to joints/servos of arm
    	self.joint1 = rospy.Publisher('/arm_shoulder_pan_joint/command',Float64)
	self.joint2 = rospy.Publisher('/arm_shoulder_lift_joint/command',Float64)
    	self.joint3 = rospy.Publisher('/arm_elbow_flex_joint/command',Float64)
    	self.joint4 = rospy.Publisher('/arm_wrist_flex_joint/command',Float64)
	self.joint5 = rospy.Publisher('/gripper_joint/command',Float64)
	self.pos1 = Float64()
    	self.pos2 = Float64()
    	self.pos3 = Float64()
    	self.pos4 = Float64()
    	self.pos5 = Float64()
	rospy.sleep(3)
	
	# Arm in "home" position
	self.pos1 = 0.000
	self.pos2 = -1.658
	self.pos3 = -2.88
	self.pos4 = -1.01
	self.pos5 = 0.000
	self.joint1.publish(self.pos1)
	self.joint2.publish(self.pos2)
	self.joint3.publish(self.pos3)
	self.joint4.publish(self.pos4)
	self.joint5.publish(self.pos5)
	rospy.sleep(3)

	self.pos1 = 0.000
	self.pos2 = 0.902
	self.pos3 = -1.892
	self.pos4 = -0.436
	self.pos5 = -0.523
	self.joint1.publish(self.pos1)
	self.joint2.publish(self.pos2)
	self.joint3.publish(self.pos3)
	self.joint4.publish(self.pos4)
	self.joint5.publish(self.pos5)
	rospy.sleep(1)

	self.pos4 = 1.57
	self.joint4.publish(self.pos4)
	rospy.sleep(1)

	self.pos1 = 0.000
	self.pos2 = 1.745
	self.pos3 = -1.57
	self.joint1.publish(self.pos1)
	self.joint2.publish(self.pos2)
	self.joint3.publish(self.pos3)
	rospy.sleep(2)	

	self.pos1 = 0.000
	self.pos2 = 1.745
	self.pos3 = -1.05
	self.pos4 = 1.178
	self.pos5 = -0.523
	self.joint1.publish(self.pos1)
	self.joint2.publish(self.pos2)
	self.joint3.publish(self.pos3)
	self.joint4.publish(self.pos4)
	self.joint5.publish(self.pos5)
	rospy.sleep(1)

	self.pos5 = 0.48
	self.joint5.publish(self.pos5)
	rospy.sleep(2)

	self.pos1 = 0.000
	self.pos2 = -0.9265
	self.pos3 = -2.387
	self.pos5 = 0.48
	self.joint1.publish(self.pos1)
	self.joint2.publish(self.pos2)
	self.joint3.publish(self.pos3)
	self.joint5.publish(self.pos5)
	rospy.sleep(1)
		
	self.pos4 = -0.30
	self.joint4.publish(self.pos4)
	rospy.sleep(2)

    def cleanup(self):
        rospy.loginfo("Shutting down crane arm....")

if __name__=="__main__":
    rospy.init_node('crane_arm')
    try:
        Loop()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
#!/usr/bin/env python
"""
"""
    turtlebot_arm.py - move turtlebot arm according to predefined gestures

"""

#The program below is used in robocup game in hefei!
import rospy
from std_msgs.msg import Float64

class Loop:
    def __init__(self):
        rospy.on_shutdown(self.cleanup)
	# publish command message to joints/servos of arm
    	self.joint1 = rospy.Publisher('/arm_shoulder_pan_joint/command',Float64)
	self.joint2 = rospy.Publisher('/arm_shoulder_lift_joint/command',Float64)
    	self.joint3 = rospy.Publisher('/arm_elbow_flex_joint/command',Float64)
    	self.joint4 = rospy.Publisher('/arm_wrist_flex_joint/command',Float64)
	self.joint5 = rospy.Publisher('/gripper_joint/command',Float64)
	self.pos1 = Float64()
    	self.pos2 = Float64()
    	self.pos3 = Float64()
    	self.pos4 = Float64()
    	self.pos5 = Float64()
	# Initial gesture of robot arm
	self.pos1 = 0
	self.pos2 = 2.219
	self.pos3 = -2.505
	self.pos4 = -1.268
	self.pos5 = -0.7
	self.joint1.publish(self.pos1)
	rospy.sleep(4)
	self.joint2.publish(self.pos2)
	self.joint3.publish(self.pos3)
	self.joint4.publish(self.pos4)
	self.joint5.publish(self.pos5)
	rospy.sleep(2)
	rospy.loginfo("Connecting to turtlebot arm....")

	while not rospy.is_shutdown():

		# gesture 1 the longth of the arm is 33cm the longth between the second motor and the turtlebot is 5 cm 
		self.pos1 = 3.14
		self.pos2 = 1.047
		self.pos3 = -2.355
		self.pos4 = 0.5
		self.pos5 = -0.7

		self.joint2.publish(self.pos2)
		self.joint3.publish(self.pos3)
		self.joint4.publish(self.pos4)
		self.joint5.publish(self.pos5)
		rospy.sleep(4)
		rospy.loginfo("Gesture 1....")

		# gesture 2 pull the gripper up
		self.pos1 = 3.14
		self.pos2 = 0
		self.pos3 = -1.396
		self.pos4 = 0.5
		self.pos5 = -0.7
		
		self.joint2.publish(self.pos2)
		self.joint3.publish(self.pos3)
		self.joint4.publish(self.pos4)
		self.joint5.publish(self.pos5)
		rospy.sleep(2)
		rospy.loginfo("Gesture 2....")
		
		# gesture 3 pull the gripper down
		self.pos1 = 3.14
		self.pos2 = 0
		self.pos3 = -1.396
		self.pos4 = 0.174
		self.pos5 = -0.7
		
		self.joint2.publish(self.pos2)
		self.joint3.publish(self.pos3)
		self.joint4.publish(self.pos4)
		self.joint5.publish(self.pos5)
		rospy.sleep(2)
		rospy.loginfo("Gesture 3....")

		# gesture 4 flate situation
		self.pos1 = 3.14
		self.pos2 = -1.396
		self.pos3 = 0
		self.pos4 = 0.174
		self.pos5 = -0.7
		
		self.joint2.publish(self.pos2)
		self.joint3.publish(self.pos3)
		self.joint4.publish(self.pos4)
		self.joint5.publish(self.pos5)
		rospy.sleep(2)
		rospy.loginfo("Gesture 4....")

		# gesture 5 catch
		self.pos1 = 3.14
		self.pos2 = -1.396
		self.pos3 = 0
		self.pos4 = 0.174
		self.pos5 = 0.5
		
		self.joint2.publish(self.pos2)
		self.joint3.publish(self.pos3)
		self.joint4.publish(self.pos4)
		self.joint5.publish(self.pos5)
		rospy.sleep(2)
		rospy.loginfo("Gesture 5....")

		# gesture 6 pull it back
		self.pos1 = 3.14
		self.pos2 = -2
		self.pos3 = 1.047
		self.pos4 = 0.174
		self.pos5 = 0.5
		
		self.joint2.publish(self.pos2)
		self.joint3.publish(self.pos3)
		self.joint4.publish(self.pos4)
		self.joint5.publish(self.pos5)
		rospy.sleep(2)
		rospy.loginfo("Gesture 6....")

		# gesture 7 lift it up
		self.pos1 = 3.14
		self.pos2 = -2
		self.pos3 = 1.147
		self.pos4 = 0.523
		self.pos5 = 0.5
		
		self.joint2.publish(self.pos2)
		self.joint3.publish(self.pos3)
		self.joint4.publish(self.pos4)
		self.joint5.publish(self.pos5)
		rospy.sleep(15)
		rospy.loginfo("Gesture 7....")

		# gesture 8 lift it down
		self.pos1 = 3.14
		self.pos2 = -2
		self.pos3 = 1.147
		self.pos4 = -0.174
		self.pos5 = 0.5
		
		self.joint2.publish(self.pos2)
		self.joint3.publish(self.pos3)
		self.joint4.publish(self.pos4)
		self.joint5.publish(self.pos5)
		rospy.sleep(2)
		rospy.loginfo("Gesture 8....")

		# gesture 9 open the gripper and pull it on the flate
		self.pos1 = 3.14
		self.pos2 = -2
		self.pos3 = 1.147
		self.pos4 = -0.214
		self.pos5 = -0.7
		
		self.joint2.publish(self.pos2)
		self.joint3.publish(self.pos3)
		self.joint4.publish(self.pos4)
		self.joint5.publish(self.pos5)
		rospy.sleep(2)
		rospy.loginfo("Gesture 9....")

		# gesture 10 pull the gripper up
		self.pos1 = 3.14
		self.pos2 = -1
		self.pos3 = 0
		self.pos4 = 0
		self.pos5 = -0.7
		
		self.joint2.publish(self.pos2)
		self.joint3.publish(self.pos3)
		self.joint4.publish(self.pos4)
		self.joint5.publish(self.pos5)
		rospy.sleep(2)
		rospy.loginfo("Gesture 10....")


		# initial gesture 
		self.pos1 = 3.14
		self.pos2 = 2.219
		self.pos3 = -2.505
		self.pos4 = -1.268
		self.pos5 = -0.7
		
		self.joint2.publish(self.pos2)
		self.joint3.publish(self.pos3)
		self.joint4.publish(self.pos4)
		self.joint5.publish(self.pos5)
		rospy.sleep(4)
		rospy.loginfo("Gesture 1....")


    def cleanup(self):
        rospy.loginfo("Shutting down turtlebot arm....")

if __name__=="__main__":
    rospy.init_node('turtlebot_arm')
    try:
        Loop()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass


"""
# new calculating algorithm
import rospy
import math
from std_msgs.msg import String
from std_msgs.msg import Float64
from test.msg import pos
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
	self.up = 1
	self.stop = 0
	self.down = 2
	# adding program
	self.nav = 0
	def callback_pos (data_pos):
		rospy.loginfo(rospy.get_caller_id() + "I heard that coordinate is %s", data_pos)
		self.x = data_pos.x
		self.y = data_pos.y
		self.z = data_pos.z
		self.rx = self.x
        # adding program
	def callback_nav (data_nav):
		rospy.loginfo( "I heard that the robot has reached the place")
		self.nav = data_nav
		print self.nav
	# adding program above
	rospy.Subscriber("pos", pos, callback_pos)
	rospy.loginfo("Subscribe to topic pos.....")
	rospy.sleep(4)
        #adding program
	rospy.Subscriber("nav_chatter", Float64, callback_nav)
	rospy.loginfo("Subscribe to topic nav_chatter.....")
	rospy.sleep(4)
	
	while self.x == 10 or self.z == 10:
	    self.a = 0.07#0.161
	    self.b = 0.25#0.2	
	    #break
	else:
	    self.a = self.x #used correct data before
	    self.b = self.y 
        while self.b < 0:
        	rospy.loginfo("This coordinate is out of my location......")
	self.l1 = 0.1957#0.161
	self.l3 = 0.1043
	rospy.loginfo("The coordinate we used to catch is .....")
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
	self.posi1 = 2.8#1.57#4.14
	self.posi2 = -1.38
	self.posi3 = 1.66
	self.posi4 = -1.57
	self.posi5 = -0.7
	rospy.sleep(2)
	rospy.loginfo("Connecting to turtlebot arm....")

	while not rospy.is_shutdown():
	
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

    def cleanup(self):
        rospy.loginfo("Shutting down turtlebot arm....")

if __name__=="__main__":

    rospy.init_node('turtlebot_arm')
    try:
        Loop()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
"""
