#!/usr/bin/env python



"""
    play riddle game
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
		#rospy.sleep(2) 


		self.riddle_turn = rospy.Publisher('turn_robot', String, queue_size=10)

		rospy.Subscriber('riddle_begin', String, self.talk_begin) 
		

	def talk_begin(self,msg):
		msg.data=msg.data.lower()
		print msg.data
		if msg.data.find('ready') > -1 :
			rospy.sleep(6)
			self.soundhandle.say('hello,I want to play riddles',self.voice)
			rospy.sleep(10)
			self.riddle_turn.publish('ok')
			rospy.Subscriber('human_num', String, self.saynum)
	def saynum(self,msg):
		msg.data=msg.data.lower()
		#print "female number is " + msg.data
		#print "male number is" + msg.data(2) 
		#self.soundhandle.say('female number is'+ msg.data,self.voice)
		self.soundhandle.say(msg.data,self.voice)
		#rospy.sleep(6)
		#self.soundhandle.say('male number is'+ msg.data(2),self.voice)
		#rospy.sleep(5)
		#self.soundhandle.say('who wants to play riddles with me',self.voice)
		#rospy.Subscriber('recognizer_output', String, self.talk_back)

	def talk_back(self, msg):
		msg.data = msg.data.lower()
		print msg.data

		if msg.data.find('shelf') > -1 or msg.data.find('the-shelf') > -1 : 
			self.soundhandle.say('the shelf is in the kitchen', self.voice)
			rospy.sleep(1)
		if msg.data.find('crowd') > -1 or msg.data.find('size') > -1 : 
			self.soundhandle.say('there are three people', self.voice)
			rospy.sleep(1)	
		if msg.data.find('chairs') > -1 or msg.data.find('dinning-room') > -1 : 
			self.soundhandle.say('there are three chairs', self.voice)
			rospy.sleep(1)	


    	def cleanup(self):
		rospy.loginfo("Shutting down gpsr node...")

if __name__=="__main__":
    rospy.init_node('gpsr')
    try:
	gpsr()
	rospy.spin()
    except:
	pass



