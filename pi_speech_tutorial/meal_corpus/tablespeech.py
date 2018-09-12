#!/usr/bin/env python

"""
    talkback.py - Say back what is heard by the pocketsphinx recognizer.
tab form!!!
"""

import roslib; roslib.load_manifest('pi_speech_tutorial')
import rospy
import datetime
import re
import time
from std_msgs.msg import String

from sound_play.libsoundplay import SoundClient

class TalkBack:
     
	def __init__(self):
		rospy.on_shutdown(self.cleanup)
		self.voice = rospy.get_param("~voice", "voice_don_diphone")
		self.wavepath = rospy.get_param("~wavepath", "")
		self.soundhandle = SoundClient()
		rospy.sleep(1)
		self.if_followme=0
		self.if_stop = 0
		self.soundhandle.stopAll()
		self.pubbring = rospy.Publisher('voice2bring', String, queue_size=10)
 		rospy.Subscriber('recognizer_output',String,self.follow)
	

	def follow(self,msg):
		msg.data=msg.data.lower()
		print msg.data
		if msg.data.find('kamerider') > -1 :
			self.pubbring.publish('kamerider')
			self.soundhandle.say('kamerider',self.voice)
			rospy.sleep(3)
			print "kamerider"

		elif msg.data.find('coffee-mate') > -1 :
			self.pubbring.publish('coffee-mated')
			self.soundhandle.say('coffee mate',self.voice)				
			rospy.sleep(3)
			print "coffee mate"

		elif msg.data.find('digestive') > -1 :
			self.pubbring.publish('digestive')
			self.soundhandle.say('digestive',self.voice)
			rospy.sleep(3)
			print "digestive"
		

	def cleanup(self):
		rospy.loginfo("Shutting down talkback node...")

if __name__=="__main__":
	rospy.init_node('talkback')
	try:
		TalkBack()
		rospy.spin()
	except:
		pass


	

