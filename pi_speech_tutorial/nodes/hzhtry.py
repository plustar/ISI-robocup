#!/usr/bin/env python

import roslib; roslib.load_manifest('pi_speech_tutorial')
import rospy
from std_msgs.msg import String
from std_msgs.msg import Int8

from sound_play.libsoundplay import SoundClient
class hzhtry:

	def __init__(self):
	
		rospy.on_shutdown(self.cleanup)
        	self.voice = rospy.get_param("~voice", "voice_cmu_us_clb_arctic_clunits")
        	self.wavepath = rospy.get_param("~wavepath", "")
        	self.soundhandle=SoundClient()
        	rospy.sleep(1)
        	self.soundhandle.stopAll()
        	rospy.sleep(1)
        	self.soundhandle.say("ready",self.voice)
        	rospy.sleep(2)
        	
        	rospy.Subscriber('recognizer_output', String, self.talk_back) 
        	
        	
        def talk_back(self,msg):
        	
        	rospy.loginfo(msg.data)
        	msg.data = msg.data.lower()
        	print msg.data
        	
        def cleanup(self):
        	rospy.loginfo("Shutting down hzhtry node...")
        	
if __name__=="__main__":
	rospy.init_node("hzhtry")
	try:
		hzhtry()
		rospy.spin()
	except:
		pass
        	
        	
        	
        	
        	
        	
        	
        	
