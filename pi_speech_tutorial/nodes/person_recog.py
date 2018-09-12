#!/usr/bin/env python



"""
    person recognition,turn around,human number,male number,female number
"""

import roslib; roslib.load_manifest('pi_speech_tutorial')
import rospy
from std_msgs.msg import String
from std_msgs.msg import Int8


from sound_play.libsoundplay import SoundClient

class gpsr:
      
	def __init__(self):

		rospy.on_shutdown(self.cleanup)
		self.voice = rospy.get_param("~voice", "voice_cmu_us_clb_arctic_clunits")
		self.wavepath = rospy.get_param("~wavepath", "")

		# Create the sound client object
		self.soundhandle = SoundClient() 
		rospy.sleep(1)
		self.soundhandle.stopAll()

		# Announce that we are ready for input
		rospy.sleep(1) 
		self.soundhandle.say("Ready", self.voice)
		rospy.sleep(2) 
		self.i=0
		self.name=''
		 
		self.start_recog=rospy.Publisher('voice2img',String,queue_size=10)

	
		self.soundhandle.say("I am ready",self.voice)
		rospy.sleep(2.5)
		self.soundhandle.say("please stand in front of me about one point five meters away and look at me",self.voice)
		rospy.sleep(4)
		self.start_recog.publish('cap_operator')

		rospy.Subscriber('img2voice',String,self.say_op)
		
		rospy.Subscriber('memorized_operator',String,self.recogok)
	def recogok(self,msg):
		msg.data=msg.data.lower()
		print msg.data
		if msg.data.find('memorized_operator')>-1:
			self.soundhandle.say('I have memorized you',self.voice)
			rospy.sleep(3)
			self.soundhandle.say('please go to the location behind me about 2 meters away',self.voice)
			rospy.sleep(10)
			self.start_recog.publish('turn_robot')
			
			rospy.Subscriber('human_num',String,self.hmnum)
			
			rospy.Subscriber('female_num',String,self.fmnum)
			
			rospy.Subscriber('male_num',String,self.mnum)
			
			rospy.Subscriber('operator_left_num',String,self.pos)
	
		
	def say_op(self,msg):
		msg.data=msg.data.lower()
		print msg.data
		self.soundhandle.say(msg.data,self.voice)
		rospy.sleep(4)
		
	def hmnum(self,msg):
		msg.data=msg.data.lower()
		print msg.data
		self.soundhandle.say("human number is "+msg.data,self.voice)
		rospy.sleep(3)
		


	def fmnum(self,msg):
		msg.data=msg.data.lower()
		print msg.data
		self.soundhandle.say("female number is "+msg.data,self.voice)
		rospy.sleep(3)

	def mnum(self,msg):
		msg.data=msg.data.lower()
		print msg.data
		self.soundhandle.say("male number is "+msg.data,self.voice)
		rospy.sleep(3)

	def pos(self,msg):
		msg.data=msg.data.lower()
		print msg.data
		self.soundhandle.say("the operator is the"+msg.data+"person on my left in the crowd",self.voice)
		rospy.sleep(8)

	def cleanup(self):
		rospy.loginfo("Shutting down gpsr node...")

if __name__=="__main__":
	rospy.init_node('gpsr')
	try:
		gpsr()
		rospy.spin()
	except:
		pass



