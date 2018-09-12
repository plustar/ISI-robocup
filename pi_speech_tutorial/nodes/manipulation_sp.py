#!/usr/bin/env python



"""
    manipulation and object recognition,speak out what it has recived 
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
		

		rospy.Subscriber('recognizer/output',String,self.sayout)

	
	def sayout(self,msg):
		msg.data=msg.data.lower()
		print msg
		self.soundhandle.say(msg.data, self.voice)
	 
	
	def cleanup(self):
		rospy.loginfo("Shutting down gpsr node...")

if __name__=="__main__":
	rospy.init_node('gpsr')
	try:
		gpsr()
		rospy.spin()
	except:
		pass
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
