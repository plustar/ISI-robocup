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
		
		self.soundhandle.say('I want to play a riddle game',self.voice)
		rospy.sleep(13)
		self.start_recog.publish('turn_robot')
		
		rospy.Subscriber('human_num',String,self.hmnum)
		
		rospy.Subscriber('female_num',String,self.fmnum)
		
		rospy.Subscriber('male_num',String,self.mnum)
			
			
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

	

	def cleanup(self):
		rospy.loginfo("Shutting down gpsr node...")

if __name__=="__main__":
	rospy.init_node('gpsr')
	try:
		gpsr()
		rospy.spin()
	except:
		pass



