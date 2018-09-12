#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
		self.names ={'name':['alex','tracy']}
		rospy.on_shutdown(self.cleanup)
		self.voice = rospy.get_param("~voice", "voice_cmu_us_clb_arctic_clunits")
		self.wavepath = rospy.get_param("~wavepath", "")

		
		# Create the sound client object
		self.soundhandle = SoundClient() 
		rospy.sleep(1)
		self.soundhandle.stopAll()
		rospy.sleep(1)
	
		self.mstype_out1 = 5
		self.mission_out1 = ''
		self.i = 0
		self.h = 0
		rospy.loginfo("To deal with the mission...")
		self.package = "voice"
		self.executable = "talker"
		self.node = roslaunch.core.Node(self.package, self.executable)
		self.launch = roslaunch.scriptapi.ROSLaunch()
		self.launch.start()
		
		
		self.pub = rospy.Publisher('mission_complete', String, queue_size=20)
		self.gpsr_name = rospy.Publisher('gpsr_name', String, queue_size=10)
		self.gpsr_missiontype1 = rospy.Publisher('gpsr_mstype_out', Int8, queue_size = 10)
		self.gpsr_mission1 = rospy.Publisher('gpsr_mission_out', String, queue_size=10)
		rospy.Subscriber('nav_output', String, self.control)
		rospy.Subscriber('gpsr_mstype', Int8, self.mstype_out)        #mission type
		rospy.Subscriber('gpsr_mission', String, self.mission_out)
		rospy.Subscriber('gpsr_mstype_out', Int8, self.mstype_out)
		rospy.Subscriber('gpsr_mission_out', String, self.mission_out)
		
		
	def mstype_out(self, msg):
		self.mstype_out1 = msg.data
		self.gpsr_missiontype1.publish(self.mstype_out1)
		
	def mission_out(self, msg):
		msg.data = msg.data.lower()
		self.mission_out1 = msg.data
		if self.i == 0:
			self.gpsr_mission1.publish(self.mission_out1)
			
	def control(self, msg):
		msg.data = msg.data.lower()
		if msg.data.find('arrive') > -1:
			rospy.Subscriber('gpsr_mstype_out', Int8, self.dispatch)

		if self.i == 0:
			os.system("rosnode kill /gpsr")          # 到达以后开始执行mission，杀死gpsr节点
			self.i = 1 
			                                                                                                                                                                                                                                                                                    
	def dispatch(self, msg):
		if self.h == 0:
			if(msg.data == 0):
				rospy.Subscriber('gpsr_mission_out', String, self.inform)
			elif(msg.data == 1):
				self.i = 1
				self.soundhandle.say("dear operator",self.voice)
				rospy.sleep(2)
				self.soundhandle.say("i am ready for your question", self.voice)
				rospy.sleep(3)
				print 555
				rospy.Subscriber('recognizer_output', String, self.answer_a_question)
			elif(msg.data == 2):
				rospy.Subscriber('gpsr_mission_out', String, self.ask_a_question)
			self.h = 1



	def inform(self, msg):
		msg.data = msg.data.lower()
		if msg.data.find('time') > -1:
			curtime = time.strftime("%H:%M %p", time.localtime())
			self.soundhandle.say("it is "+ curtime, self.voice)
			rospy.sleep(5)
		os.system("rosnode kill /talkback")
		
	def answer_a_question(self, msg):
		msg.data = msg.data.lower()
		if msg.data.find('kamerider') > -1:
			if msg.data.find('first-president') > -1 or msg.data.find('the-usa') > -1 : 
				self.soundhandle.say('george washington was the first president of america', self.voice)
				rospy.sleep(4)
			elif msg.data.find('titanic built') > -1 or msg.data.find('titanic-built') > -1 or msg.data.find('in which city') > -1 :
				self.soundhandle.say('titanic was builted in belfast', self.voice)
				rospy.sleep(4)
			elif msg.data.find('queen-victoria') > -1 or msg.data.find('how-many-children') > -1 :
				self.soundhandle.say('she had nine children', self.voice)
				rospy.sleep(4)
			elif msg.data.find('another-name') > -1 or msg.data.find('study of fosslis') > -1 or msg.data.find('study the fosslis') > -1 or msg.data.find('study-of-the-fosslis') > -1 : 
				self.soundhandle.say('the another name for the study of fossils is paleontology', self.voice)
				rospy.sleep(4)
			elif msg.data.find('dragonflies') > -1 or msg.data.find('prefer-to-eat') > -1 : 
				self.soundhandle.say('dragonfilies prefer to eat mosquitoes', self.voice)
				rospy.sleep(4)	
			elif msg.data.find('cannot-fly') > -1 or msg.data.find('but can jump') > -1 : 
				self.soundhandle.say('they are fleas', self.voice)
				rospy.sleep(4)
			elif msg.data.find('color-is-cobalt') > -1 or msg.data.find('cobalt') > -1 : 
				self.soundhandle.say('the color of cobalt is blue', self.voice)
				rospy.sleep(4)
			elif msg.data.find('which device') > -1 or msg.data.find('use to look at') > -1 or msg.data.find('at-the-stars') > -1 or msg.data.find('at-stars') > -1 : 
				self.soundhandle.say('we also use telescope to look at the stars', self.voice)
				rospy.sleep(4)
			elif msg.data.find('light-intensity') > -1 : 
				self.soundhandle.say('candela also indicates the light intensity', self.voice)
				rospy.sleep(4)
			elif msg.data.find('first-american') > -1 : 
				self.soundhandle.say('alan shepard was the first american in space', self.voice)
				rospy.sleep(4)			
			elif msg.data.find('planet') > -1 or msg.data.find('nearest-the-sun') > -1 : 
				self.soundhandle.say('the planet nearest-the-sun is mercury', self.voice)
				rospy.sleep(4)
			elif msg.data.find('great-wall') > -1 : 
				self.soundhandle.say('it is six thousand two hundred fifty-nine kilometers', self.voice)
				rospy.sleep(4)
			elif msg.data.find('largest-number') > -1 or msg.data.find('five-digits') > -1 : 
				self.soundhandle.say('the largest number of five digits is ninty-nine thousand nine hundred and ninty-nine', self.voice)
			else :
				self.soundhandle.say('Dear opreater', self.voice)
				rospy.sleep(1.5)
				self.soundhandle.say('Please repeat your question louder and slower', self.voice)
				rospy.sleep(3)
			msg.data = ''
		os.system("rosnode kill /talkback")

	def ask_a_question(self, msg):
		msg.data = msg.data.lower()
		if msg.data.find('name') > -1:
			self.soundhandle.say("what is your name", self.voice) 
			rospy.sleep(5)
			rospy.Subscriber('recognizer_output', String, self.lis_to_ans)
		
	
	def get_keyword(self, data):
		for (temp, keywords) in self.names.iteritems():
			for word in keywords:
				if data.find(word) > -1:
					return word
		return 'None'

	def lis_to_ans(self, msg):
		msg.data = msg.data.lower()
		keyword = self.get_keyword(msg.data)
		if keyword != 'None':
			self.soundhandle.say("Hello " + keyword, self.voice)
			rospy.sleep(10)
			
			self.temp_pub = rospy.Publisher('information', String, queue_size=20)
			keyword = self.get_keyword(msg.data)
			self.temp_pub.publish(keyword)
			keyword = 'None'
			os.system("rosnode kill /talkback")	
			os.system("rosnode kill /soundplay_node")	
			os.system("rosnode kill /talker")
			os.system("rosnode kill /server2topic")		
	def cleanup(self):
		rospy.loginfo("Shutting down talkback node...")


if __name__=="__main__":	
	rospy.init_node('talkback')
	try:
	#rospy.Subscriber('nav_output', String, self.control) 
		TalkBack()
		rospy.spin()
	except:
		pass

