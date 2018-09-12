#!/usr/bin/env python

"""
    talkback.py - Say back what is heard by the pocketsphinx recognizer.
"""

import roslib; roslib.load_manifest('pi_speech_tutorial')
import rospy
import datetime
import re
import time
from std_msgs.msg import String
from std_msgs.msg import Int8
import roslaunch
import os

from sound_play.libsoundplay import SoundClient

class TalkBack:
      
    def __init__(self):
        rospy.on_shutdown(self.cleanup)
        self.voice = rospy.get_param("~voice", "voice_don_diphone")
        self.wavepath = rospy.get_param("~wavepath", "")
        
#	self.open_object_name = rospy.Publisher('open_object_name', String, queue_size=10)
        # Create the sound client object
        self.soundhandle = SoundClient()
        rospy.sleep(1)
        self.soundhandle.stopAll()
#	self.ready = 0
        # Announce that we are ready for input
#       self.soundhandle.playWave(self.wavepath + "/R2D2a.wav")
	rospy.sleep(20)
	self.soundhandle.say("ready", self.voice)
	rospy.sleep(3)

        #rospy.loginfo("Say one of the navigation commands...")

        # self.open_object_name = rospy.Publisher('open_object_name', String, queue_size=10)
        # rospy.init_node('command', anonymous=True)

        # Subscribe to the recognizer output
        # rospy.Subscriber('speech_recognition_start', String, self.start)
	rospy.Subscriber('recognizer_output', String, self.recognition)
    def recognition(self, msg) :
	msg.data = msg.data.lower()
	print msg.data
	if msg.data.find('kamerider') > -1:
		self.soundhandle.playWave(self.wavepath + "/R2D2a.wav")
		rospy.sleep(1)
		
		if msg.data.find('time') > -1 or msg.data.find('what-time') > -1: 
			curtime = time.strftime("%H:%M %p", time.localtime())
			self.soundhandle.say("it is "+ curtime, self.voice)
			rospy.sleep(6)
		elif msg.data.find('orange') > -1 or msg.data.find('like-orange') > -1 or msg.data.find('like-apple') > -1: 
			self.soundhandle.say('I like apple more than orange', self.voice)
			rospy.sleep(6)
		elif msg.data.find('how-old') > -1 or msg.data.find('old') > -1 : 
			self.soundhandle.say('I am five years old', self.voice)
			rospy.sleep(6)
		elif msg.data.find('live') > -1 or msg.data.find('where-are-you-from') > -1 : 
			self.soundhandle.say('I am from NanKai University', self.voice)
			rospy.sleep(6)
		elif msg.data.find('are-you-boy') > -1 or msg.data.find('are-you-girl') > -1 : 
			self.soundhandle.say('I am a boy', self.voice)
			rospy.sleep(6)
		elif msg.data.find('first-american') > -1 : 
			self.soundhandle.say('alan shepard was the first american in space', self.voice)
			rospy.sleep(6)
		elif msg.data.find('largest-number') > -1 or msg.data.find('five-digits') > -1 : 
			self.soundhandle.say('the largest number of five digits is ninty-nine thousand nine hundred and ninty-nine', self.voice)
		else :
			print msg.data
			self.soundhandle.say('Dear opreater', self.voice)
			rospy.sleep(1.5)
			self.soundhandle.say('Please repeat your question louder and slower', self.voice)
			rospy.sleep(6)
		msg.data = ''
		#self.soundhandle.say('now you can ask another question', self.voice)
		#rospy.sleep(3)


    def cleanup(self):
        rospy.loginfo("Shutting down talkback node...")

if __name__=="__main__":
    rospy.init_node('talkback')
    try:
        TalkBack()
        rospy.spin()
    except:
        pass

