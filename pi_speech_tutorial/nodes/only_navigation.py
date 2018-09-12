#!/usr/bin/env python


"""
    navigation.py - Say back what is heard by the pocketsphinx recognizer.
"""

import roslib; roslib.load_manifest('pi_speech_tutorial')
import rospy
from std_msgs.msg import String
from std_msgs.msg import Int8

from sound_play.libsoundplay import SoundClient

class navsp:
      
	def __init__(self):

		rospy.on_shutdown(self.cleanup)
		self.voice = rospy.get_param("~voice", "voice_cmu_us_clb_arctic_clunits")
		self.wavepath = rospy.get_param("~wavepath", "")
		self.soundhandle=SoundClient()
		rospy.sleep(1)
		self.soundhandle.stopAll()
		rospy.sleep(2)
		self.soundhandle.say("ready",self.voice)

		rospy.sleep(3)
		rospy.Subscriber('Point',String,self.nav_sp)

	def nav_sp(self,msg):
		msg.data=msg.data.lower()
		print msg
		if msg.data.find('a') > -1:
			self.soundhandle.say("I am going to move now",self.voice)
		if msg.data.find('b') > -1:
			self.soundhandle.say("I have arrived the waypoint one",self.voice)
		if msg.data.find('move') > -1:
			self.soundhandle.say("I see a man,Please move away",self.voice)
		if msg.data.find('c') >-1:
			self.soundhandle.say("I have arrived the waypoint two",self.voice)
		if msg.data.find('d')>-1:
			self.soundhandle.say("I have arrived the third point",self.voice)
			rospy.sleep(3)
			self.soundhandle.say("waiting for your command",self.voice)
			rospy.sleep(3)
			self.soundhandle.say("Please stand two meters away from me",self.voice)
			rospy.sleep(4)
			self.soundhandle.say("Dear operator",self.voice)
			rospy.sleep(2)
			self.soundhandle.say("if you say follow me",self.voice)
			rospy.sleep(3)
			self.soundhandle.say("I will start to follow you",self.voice)
			rospy.sleep(3)
			self.soundhandle.say("If you say stop follow me",self.voice)
			rospy.sleep(3)
			self.soundhandle.say("I will stop doing it",self.voice)

	def cleanup(self):
		rospy.loginfo("shuting down navsp node ....")

if __name__=="__main__":
	rospy.init_node('navsp')
	try:
		navsp()
		rospy.spin()
	except:
		pass



















